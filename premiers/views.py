from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Appointment, MainPurpose, SubPurpose, Vip
from django.http import JsonResponse
from .forms import VipForm, PurposeForm
from fuzzy.views import fuzzy
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView


def home(request):
    return render(request, 'premiers/home.html', {'title': 'Home'})


def booklist(request):
    return render(request, 'premiers/booklist.html', {'title': 'Booklist'})


def event(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'premiers/event.html', context)


def status(request):
    obj = Appointment.objects.get(id=1)
    context = {
        'object': obj
    }
    return render(request, 'premiers/status.html', context)


def vip(request):
    form = VipForm()

    if request.method == 'POST':
        form = VipForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('ezz-purpose')
    context = {
        'title': 'VIP DETAILS',
        'form': form,
    }

    return render(request, 'meetings/vip.html', context)


def sitem(request):
    form = PurposeForm()

    context = {
        'form': form
    }
    return render(request, 'meetings/purposeitem.html', context)


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

        print(" SUB ID ------>", sub.id)
        print(" SUB Weightage ----->", sub.sub_weight)
        print(" MAIN ID ------>", main.id)
        print("MAIN WEIGHTAGE", main.main_weight)
        fuzzy_result = round(fuzzy(main.main_weight, sub.sub_weight))
        print("Fuzzy : -------> ", fuzzy_result)

        if fuzzy_result > 70:
            category = "GLORY"
        elif fuzzy_result > 45 & fuzzy_result < 70:
            category = "MASTER"
        else:
            category = "ELITE"

        context = {
            'subs': sub,
            'category': category,
        }
        return context


def testing(request):
    # context = JsonResponse({'events': Event.objects.all()})
    #
    # context = {
    #     'events': Event.objects.all()
    # }
    #
    data = list(Event.objects.values())

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




