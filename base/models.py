from datetime import datetime

from django.db import models

JENIS_KELAMIN = (
        ("1",'Laki-laki'), 
        ("2",'Perempuan')
        )
class Guest(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(choices = JENIS_KELAMIN, default = '1', max_length = 1)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    needs = models.TextField()
    reserve_time = models.DateTimeField()
    created = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['reserve_time','-created']
    
    @property
    def get_date(self):
        return str(datetime.strptime(self.reserve_time, '%d-%m-%Y %H:%M:%S'))
    
    def html_date(self):
        return str(datetime.strptime(self.reserve_time, '%Y-%m-%d %H:%M:%S'))
    
    def get_year(self):
        return str(datetime.strftime(self.reserve_time, "%Y"))
    
    def get_month(self):
        return str(datetime.strftime(self.reserve_time, "%m"))

    def get_day(self):
        return str(datetime.strftime(self.reserve_time, "%d"))
    
    def __str__(self):
        return self.name
    
    
    
# Create your models here.
