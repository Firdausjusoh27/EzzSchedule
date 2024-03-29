from datetime import *
import datetime
from django.shortcuts import render, redirect
from events.models import Event, Slot
from premiers.models import PurposeDetail
from dateutil.parser import parse


def confirm(request):
    if request.method == "POST":
        data = request.POST
        meeting_ID = data.get('meetingId')
        selected_slot = data.get('slot')
        selected = data.get('submit')
        print("---------------------->", meeting_ID)
        print("---------------------->", selected_slot)
        print("---------------------->", selected)
        slot = Slot.objects.get(id=selected_slot)
        # print("slot----------------->", slot)
        # print(slot.start_time)
        # print(slot.end_time)
        # schedule = Event.objects.filter(id=1).values()
        # fuzzy_percent = PurposeDetail.objects.get(id=meeting_ID)
        # a = fuzzy_percent.fuzzy_weight
        # print("Fuzzy Percentage At Confirm ------->", a)
        selected_date = parse(selected)
        schedule_save = Event(user=request.user, purposeitem_id=meeting_ID, day=selected_date, start_time=slot.start_time, end_time=slot.end_time)
        print("success", schedule_save.save())
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
        PurposeDetail.objects.last().delete()
        print("Delete Slot ------------------->")
        return redirect('premiers-home')
    context = {'slot': cancel_slot}
    # https://getbootstrap.com/docs/4.0/components/modal/
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




