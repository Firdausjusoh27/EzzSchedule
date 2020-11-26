from django.urls import path
from . import views


urlpatterns = [
    path('purpose/', views.purpose, name='ezz-purpose'),
    path('vip/', views.vip, name='ezz-vip'),
]