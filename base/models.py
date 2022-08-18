from datetime import datetime
from venv import create
from django.db import models

class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    needs = models.TextField()
    reserve_time = models.DateTimeField()
    
    created = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['-created']
    
    @property
    def get_date(self):
        return str(datetime.strptime(self.reserve_time, '%d-%m-%Y %H:%M:%S'))
    
    def get_month(self):
        return str(datetime.strftime(self.reserve_time, "%m"))

    def get_day(self):
        return str(datetime.strftime(self.reserve_time, "%d"))
    
    def __str__(self):
        return self.name
    
    
    
# Create your models here.
