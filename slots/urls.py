from django.urls import path
from . import views


urlpatterns = [
    path('confirm/', views.confirm, name='ezz-confirm'),
    path('select/', views.select, name='ezz-select'),
    path('poll/', views.poll, name='poll'),
    path('pulling/', views.pulling, name='pulling'),
]

