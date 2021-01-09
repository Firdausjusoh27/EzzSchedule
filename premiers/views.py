from django.shortcuts import render, redirect
from .models import EventDummy, Appointment, MainPurpose, SubPurpose, Vip, PurposeDetail, Representative
from events.models import Event, Slot, iSlot
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from .forms import VipForm
from fuzzy.views import fuzzy
from datetime import *
import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView


def home(request):
    return render(request, 'premiers/home.html', {'title': 'Home'})


def teaser(request):
    all_slot = iSlot.objects.filter(purpose_id=24)
    print(all_slot)
    context = {
        'slots': all_slot
    }

    return render(request, 'premiers/teaser.html', context)


def about(request):
    return render(request, 'premiers/about.html', {'title': 'About'})


def booklist(request):
    return render(request, 'premiers/booklist.html', {'title': 'Booklist'})


def event(request):
    context = {
        'events': EventDummy.objects.all()
    }
    return render(request, 'premiers/event.html', context)


def status(request):
    logged_in_user = request.user
    logged_in_user_slots = Event.objects.filter(user=logged_in_user)
    print("------------------------------->", logged_in_user_slots)

    if logged_in_user_slots.exists():
        context = {
            'slots': logged_in_user_slots,
        }
        return render(request, 'premiers/status.html', context)

    else:
        return render(request, 'premiers/nostatus.html')


def vip(request):
    try:
        if request.method == 'POST':
            form = VipForm(request.POST)
            if form.is_valid():
                vip_form = form.save(commit=False)
                vip_form.user = request.user
                vip_form.save()
            return redirect('ezz-purpose')
        else:
            user = request.user.vip
            vip_detail = Vip.objects.get(name=user)
            context = {
                'vip': vip_detail,
            }

    except Vip.DoesNotExist:
        form = VipForm()
        context = {
            'title': 'VIP DETAILS',
            'form': form,
        }

    return render(request, 'meetings/vip.html', context)


def updateVip(request, pk):
    vip = Vip.objects.get(id=pk)
    form = VipForm(instance=vip)

    if request.method == 'POST':
        form = VipForm(request.POST, instance=vip)
        if form.is_valid():
            form.save()
            return redirect('ezz-purpose')

    context = {
        'form': form,
    }
    return render(request, 'meetings/vipupdate.html', context)


class purposedetail(TemplateView):
    template_name = "meetings/purposedetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get id from request url
        main_id = self.kwargs['pro_id']
        detail = MainPurpose.objects.get(id=main_id)
        sub_detail = SubPurpose.objects.filter(main_purpose_id=main_id)
        print("------------------->", detail)
        print("------------------>", detail.description)
        context = {
            'main_detail': detail,
            'sub_detail': sub_detail,
        }

        return context


class purpose(TemplateView):
    template_name = 'meetings/purpose.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mains'] = MainPurpose.objects.all()
        return context


class subpurpose(TemplateView):
    template_name = "meetings/subpurpose.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get id from request url
        main_id = self.kwargs['pro_id']
        # filter product by id

        context['subs'] = SubPurpose.objects.filter(main_purpose_id=main_id)
        return context


def cancel_select(request, pk):
    cancel_slot = PurposeDetail.objects.get(id=pk)
    cancel_slot.delete()
    return redirect('premiers-home')


def check_overlap(fixed_start, fixed_end, new_start, new_end):
    overlap = False
    if new_start == fixed_end or new_end == fixed_start:  # edge case
        overlap = False
    elif (new_start >= fixed_start and new_start <= fixed_end) or (
            new_end >= fixed_start and new_end <= fixed_end):  # innner limits
        overlap = True
    elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
        overlap = True

    return overlap


# function to get weekday list
def weekday_list(time_range, base):
    date_list = [base + datetime.timedelta(days=x) for x in range(time_range)]
    weekday = []
    weekdays = [5, 6]
    for dt in date_list:
        if dt.weekday() not in weekdays:  # to print only the weekdates
            print(dt.strftime("%Y-%m-%d"))
            weekday.append(dt)
    return weekday


class recommend(TemplateView):
    template_name = "meetings/recommend.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get id from request url
        sub_id = self.kwargs['pro_id']
        # filter product by id
        sub = SubPurpose.objects.get(id=sub_id)
        main = MainPurpose.objects.get(id=sub.main_purpose_id)
        fuzzy_result = round(fuzzy(main.main_weight, sub.sub_weight))
        print("Fuzzy Result ------------------->", fuzzy_result)

        purpose_detail = PurposeDetail(user=self.request.user, vip=self.request.user.vip, main_purpose=main,
                                       sub_purpose=sub, fuzzy_weight=fuzzy_result)
        purpose_detail.save()
        newid = PurposeDetail.objects.last().id
        purposeDetail = PurposeDetail.objects.get(id=newid)
        print("NEW ID", newid)

        selected_slot = Slot.objects.all()
        time_range = 10
        base = datetime.date.today()

        # Glory Category find free day within 5 workings day & the special thing is Xera open special slot.
        if fuzzy_result > 70:
            category = "GLORY"
            print(category)
            date_list = weekday_list(time_range, base)
            free_date = []
            selected_date = []
            count = 0

            save_detail = PurposeDetail.objects.get(id=newid)
            save_detail.category = category
            save_detail.fuzzy_weight = fuzzy_result
            save_detail.representative = Representative.objects.get(id=1)
            save_detail.save()

            for x in date_list:
                events = Event.objects.filter(day=x)
                print("Events", events)
                if events.exists():
                    print("There is event on this date", x)
                    if len(events) == 1:
                        for event in events:
                            for slot in selected_slot:
                                if check_overlap(event.start_time, event.end_time, slot.start_time, slot.end_time):
                                    print('There is overlap on :' + str(event.day) + ' ' + str(slot.name) + ' ' + str(slot.start_time) + '-' + str(slot.end_time))
                                else:
                                    print('This slot not overlap: ' + str(event.day) + ' ' + str(slot.name) + ' ' + str(slot.start_time) + '-' + str(slot.end_time))
                                    i_slot = iSlot(purpose_id=purposeDetail, date=event.day, slot=slot)
                                    i_slot.save()
                                    print("Success Save iSlot")
                                    count = count+1
                else:
                    for slot in selected_slot:
                        if count < 6:
                            i_slot = iSlot(purpose_id=purposeDetail, date=x, slot=slot)
                            i_slot.save()
                            count = count+1
                    print("No Event", x)

            print("")
            all_slot = iSlot.objects.filter(purpose_id=newid)
            print(all_slot)

            context = {
                'mains': main,
                'subs': sub,
                'category': category,
                'selected_date': selected_date,
                'purposeDetail': purposeDetail,
                'selected_slot': selected_slot,
                'all_slot': all_slot,
            }
            return context

        # Master Category just find free day within 14 workings day
        elif 45 <= fuzzy_result <= 70:
            category = "MASTER"
            print(category)
            next_week = base
            date_list = weekday_list(time_range, next_week)
            free_date = []
            selected_date = []

            save_detail = PurposeDetail.objects.get(id=newid)
            save_detail.category = category
            save_detail.fuzzy_weight = fuzzy_result
            save_detail.representative = Representative.objects.get(id=1)
            save_detail.save()

            for x in date_list:
                events = Event.objects.filter(day=x)
                if events.exists():
                    print("There is event on this date", x)
                else:
                    free_date.append(x)
                    print("No Event", x)

        # Elite Category just find free day within 30 workings day
        else:
            category = "ELITE"
            print(category)
            next_week = base
            date_list = weekday_list(time_range, next_week)
            free_date = []
            selected_date = []
            save_detail = PurposeDetail.objects.get(id=newid)
            save_detail.category = category
            save_detail.fuzzy_weight = fuzzy_result
            save_detail.representative = Representative.objects.get(id=2)
            save_detail.save()

            # Loop function to find free or busy day in calendar
            for x in date_list:
                events = Event.objects.filter(day=x)
                selected_slot = Slot.objects.all()
                if events.exists():
                    for event in events:
                        for slot in selected_slot:
                            if check_overlap(event.start_time, event.end_time, slot.start_time, slot.end_time):
                                print('There is overlap on :' + str(event.day) + str(event.start_time) + '-' + str(event.end_time))
                else:
                    free_date.append(x)
                    print("No Event", x)

        for y in range(3):
            selected_date.append(free_date[y])

        print("selected date --------------->", selected_date)
        context = {
            'mains': main,
            'subs': sub,
            'category': category,
            'selected_date': selected_date,
            'purposeDetail': purposeDetail,
            'selected_slot': selected_slot,
        }
        return context

    # Fuzzy Result
    # print(" SUB ID ------>", sub.id)
    # print(" SUB Weightage ----->", sub.sub_weight)
    # print(" MAIN ID ------>", main.id)
    # print("MAIN WEIGHTAGE", main.main_weight)

    # print("Fuzzy : -------> ", fuzzy_result)

    # if self.request.user.vip is not None:
    #     user = self.request.user.vip
    #     # vip_detail = Vip.objects.filter(name=user)
    #     vip_detail2 = Vip.objects.get(name=user)
    #     vip_name = user
    #     vip_email = vip_detail2.email
    #     vip_company = vip_detail2.company
    #
    #     print("Userrrrrrrrrrrrr", user)
    #     print(vip_name)
    #     print(vip_email)
    #     print(vip_company)