from datetime import *
import datetime
from django.shortcuts import render, redirect
from events.models import Event, Slot
from dateutil.parser import parse

from django.views.generic import DetailView, TemplateView
from django.http import HttpResponse, request


# Create your views here.
#
# def confirm(request):
#     if request.method == "POST":
#         meeting_date = request.POST.get('meeting_date')
#
#     return render(request, 'slots/confirm.html')


# class confirm(TemplateView):
#     template_name = "slots/confirm.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # get id from request url
#         selected_date = self.kwargs['pro_id']
#         print("Selected Date---->", selected_date)
#         # filter product by id
#         context = {
#             'selected_date': selected_date,
#         }
#         return context

def confirm(request):
    if request.method == "POST":
        data = request.POST
        meeting_ID = data.get('meetingId')
        selected_slot = data.get('slot')
        selected = data.get('submit')
        # print("---------------------->", meeting_ID)
        # print("---------------------->", selected)
        # print("---------------------->", selected_slot)
        slot = Slot.objects.get(id=selected_slot)
        # print("slot----------------->", slot)
        # print(slot.start_time)
        # print(slot.end_time)
        # schedule = Event.objects.filter(id=1).values()
        selected_date = parse(selected)
        schedule_save = Event(user=request.user, purposeitem_id=meeting_ID, day=selected_date, start_time=slot.start_time, end_time=slot.end_time)
        # print("success", schedule_save.save())
        # print(schedule)
        new_id = Event.objects.last().id
        created_event = Event.objects.get(id=new_id)

    context = {
        'selected_date': selected,
        'created_event': created_event
    }
    return render(request, "slots/confirm.html", context)


def cancelSlot(request, pk):
    cancel_slot = Event.objects.get(id=pk)
    if request.method == 'POST':
        cancel_slot.delete()
        print("Delete Slot ------------------->")
        return redirect('premiers-home')
    context = {'slot': cancel_slot}
    return render(request, 'slots/cancel.html', context)



def select(request):
    return render(request, 'slots/select.html', {'title': 'Select'})


def pulling(request, id=None):
    if request.method == "POST":
        data = request.POST
        choice = data['answer']
        choice2 = request.POST.get('answer2')
        print("---------------------------->", choice)
        print("---------------------------->222", choice2)
    context = {
        'data': "pulling",
    }
    return render(request, "slots/pulling.html", context)


def poll(request):
    time_range = 3
    base = datetime.date.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(time_range)]
    print("Date Listtttt", date_list)
    context = {
        'data': "poll",
        'date_list': date_list,
    }
    return render(request, "slots/poll.html", context)




