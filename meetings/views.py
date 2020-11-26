from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


# Create your views here.

def purpose(request):
    return render(request, 'meetings/purpose.html', {'title': 'Meeting'})


def vip(request):
    context = [
        {'title': 'Vip'}
    ]
    return render(request, 'meetings/vip.html', context)