from django.urls import path
from . import views


urlpatterns = [
    path('confirm/<str:pro_id>', views.confirm.as_view(), name='ezz-confirm'),
    path('select/', views.select, name='ezz-select'),
]

