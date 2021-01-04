from django.urls import path
from . import views


urlpatterns = [
    path('', views.event, name='premiers-event'),
    path('home/', views.home, name='premiers-home'),
    path('book/', views.booklist, name='premiers-book'),
    path('status/', views.status, name='premiers-status'),
    path('testing/', views.testing, name='premiers-testing'),
    path('vip/', views.vip, name='ezz-vip'),
    path('purpose/', views.purpose.as_view(), name='ezz-purpose'),
    path('subpurpose/<int:pro_id>', views.subpurpose.as_view(), name='ezz-subpurpose'),
    path('recommend/<int:pro_id>', views.recommend.as_view(), name='ezz-recommend'),
    path('category/', views.CategoryView.as_view(), name='ezz-category'),
    path('all-subs/', views.AllSubView.as_view(), name='allsubs'),
    path('subcategory/<int:pro_id>', views.CategoryDetailView.as_view(), name='subcategory'),
    path('vipupdate/<str:pk>', views.updateVip, name='premiers-vip'),
    path('purposedetail/<int:pro_id>', views.purposedetail.as_view(), name='ezz-purposedetail'),

]
