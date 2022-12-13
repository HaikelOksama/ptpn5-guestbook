from django.contrib import admin
from .models import Guest
# Register your models here.

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "reserve_time")
    list_filter = ("reserve_time",)
    search_fields = ("name", )