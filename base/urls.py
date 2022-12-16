from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("tamu/", views.guest_view, name='guest'),
    path("login/", views.login_view, name="login"),
   
    path("logout/", views.logout_user, name="logout"),
    
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('guest-list/', views.guest_list_view, name='guest-list'),
    
    path('monthly/', views.monthly_data_view, name='monthly-data'),
    
    path('new-guest/', views.new_guest_view, name='create'),
    path('guest/<int:pk>/', views.new_guest_view, name='edit'),
    
    path('delete/<int:pk>', views.delete_guest_view, name='delete'),
    
    path('statistic/', views.statistic_view, name='statistic'),

    path('export/', views.export_view, name='export'),
    path('export/<int:year_par>/', views.export_view, name='export-year'),
    path('export/<int:year_par>/<int:month_par>/', views.export_view, name='export-month'),
    
]

