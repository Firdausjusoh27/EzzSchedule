from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def confirm(request):
    return render(request, 'slots/confirm.html', {'title': 'Confirm'})


def select(request):
    return render(request, 'slots/select.html', {'title': 'Select'})

