from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('guest-list/', views.guest_list_view, name='guest-list'),
    
    path('monthly/', views.monthly_data_view, name='monthly-data'),
    
    path('new-guest/', views.new_guest_view, name='create'),
    path('delete/<int:pk>', views.delete_guest_view, name='delete'),
    
    path('statistic/', views.statistic_view, name='statistic'),

]

