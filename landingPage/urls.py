from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_guest_view, name='guest')
]
