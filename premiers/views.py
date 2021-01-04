from django.shortcuts import render, redirect
from .models import EventDummy, Appointment, MainPurpose, SubPurpose, Vip, PurposeDetail
from events.models import Event, Slot
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

    context = {
        'slots': logged_in_user_slots,
    }
    return render(request, 'premiers/status.html', context)


# def vip(request):
#
#     # if request.user.vip is not None:
#     #     user = request.user.vip
#     #     print("Userrrrrrrrrrrrr", user)
#     # if else to check Vip have register or not
#     # if have just confirm back this VIP
#     # can edit new VIP if have changes
#
#     form = VipForm()
#
#     if request.method == 'POST':
#         form = VipForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('ezz-purpose')
#     context = {
#         'title': 'VIP DETAILS',
#         'form': form,
#     }
#
#     return render(request, 'meetings/vip.html', context)


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


# def sitem(request):
#     form = PurposeForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'meetings/purposeitem.html', context)

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


class recommend(TemplateView):
    template_name = "meetings/recommend.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get id from request url
        sub_id = self.kwargs['pro_id']
        # filter product by id
        sub = SubPurpose.objects.get(id=sub_id)
        main = MainPurpose.objects.get(id=sub.main_purpose_id)

        purpose_detail = PurposeDetail(user=self.request.user, vip=self.request.user.vip, main_purpose=main,
                                       sub_purpose=sub)
        # purpose_detail.save()
        newid = PurposeDetail.objects.last().id
        purposeDetail = PurposeDetail.objects.get(id=newid)
        print("NEW ID", newid)
        fuzzy_result = round(fuzzy(main.main_weight, sub.sub_weight))
        selected_slot = Slot.objects.all()

        if fuzzy_result > 70:
            category = "GLORY"
            time_range = 5
            base = datetime.date.today()
            date_list = [base + datetime.timedelta(days=x) for x in range(time_range)]
            print("Date Listtttt", date_list)
            free_date = []
            selected_date = []

            for x in date_list:
                events = Event.objects.filter(day=x)
                if events.exists():
                    print("There is event on this date", x)
                else:
                    free_date.append(x)
                    print("No Event", x)
            print(free_date)

        elif fuzzy_result > 45 & fuzzy_result < 70:
            category = "MASTER"
            time_range = 5
            base = datetime.date.today()
            next_week = base + datetime.timedelta(days=7)
            date_list = [next_week + datetime.timedelta(days=x) for x in range(time_range)]
            free_date = []
            selected_date = []

            for x in date_list:
                events = Event.objects.filter(day=x)
                if events.exists():
                    print("There is event on this date", x)
                else:
                    free_date.append(x)
                    print("No Event", x)

        else:
            category = "ELITE"
            time_range = 5
            base = datetime.date.today()
            next_week = base + datetime.timedelta(days=14)
            date_list = [next_week + datetime.timedelta(days=x) for x in range(time_range)]
            free_date = []
            selected_date = []

            for x in date_list:
                events = Event.objects.filter(day=x)
                if events.exists():
                    print("There is event on this date", x)
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


def testing(request):
    # context = JsonResponse({'events': Event.objects.all()})
    #
    # context = {
    #     'events': Event.objects.all()
    # }
    #
    data = list(EventDummy.objects.values())

    return JsonResponse(data, safe=False)
    # return render(request, 'premiers/testing.html')


class CategoryView(TemplateView):
    template_name = 'meetings/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mains'] = MainPurpose.objects.all()
        return context


class AllSubView(TemplateView):
    template_name = 'meetings/detailcategory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mains'] = MainPurpose.objects.all()
        return context


class CategoryDetailView(TemplateView):
    template_name = "meetings/categorydetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get id from request url
        main_id = self.kwargs['pro_id']
        print(main_id, "****************************************")
        # filter product by id

        context['subs'] = SubPurpose.objects.filter(main_purpose_id=main_id)
        return context
