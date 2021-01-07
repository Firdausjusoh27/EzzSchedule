from django.urls import path
from . import views


urlpatterns = [
    path('', views.event, name='premiers-event'),
    path('home/', views.home, name='premiers-home'),
    path('book/', views.booklist, name='premiers-book'),
    path('status/', views.status, name='premiers-status'),
    path('about/', views.about, name='premiers-about'),
    path('vip/', views.vip, name='ezz-vip'),
    path('purpose/', views.purpose.as_view(), name='ezz-purpose'),
    path('subpurpose/<int:pro_id>', views.subpurpose.as_view(), name='ezz-subpurpose'),
    path('recommend/<int:pro_id>', views.recommend.as_view(), name='ezz-recommend'),
    path('vipupdate/<str:pk>', views.updateVip, name='premiers-vip'),
    path('purposedetail/<int:pro_id>', views.purposedetail.as_view(), name='ezz-purposedetail'),
    path('cancel-select/<str:pk>', views.cancel_select, name='cancel-select'),
    path('teaser', views.teaser, name='landing-page'),

]
