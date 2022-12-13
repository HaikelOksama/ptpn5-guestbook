
import datetime
from django import forms

from django.forms import ModelForm
from .models import Guest

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class GuestForms(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))   
          
    
    class Meta:
        get_datetime = datetime.datetime.now()
        stripped_time = get_datetime.strftime('%Y-%m-%dT%H:%M')
        # stripped_time = None
        model = Guest
        fields = '__all__'
        exclude = ['created']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Masukkan Nama Anda',
                'class': 'form-control',
                }),
            'gender': forms.Select(attrs={
                'placeholder': 'Masukkan Nama Anda',
                'class': 'form-control',
                }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Alamat Email Anda',
                'class': 'form-control',
                }),
            'address': forms.TextInput(attrs={
               'placeholder': 'Alamat Tempat Tinggal Anda' ,
               'class': 'form-control',
            }),
            'reserve_time' : forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type':'datetime-local',
                
                }),
            'phone' : forms.TextInput(attrs={
                'class': 'form-control',
                'type' : 'number','placeholder': 'Berisi angka < 15 Digit'
                }),
            'needs': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jelaskan Keperluan Anda'
                }),
        }
        labels = {
            'name': "Nama",
            'gender': "Jenis Kelamin",
            'email': "E-mail (opsional)",
            'address': "Alamat",
            'needs': "Keperluan",
            'reserve_time': "Jadwal Kedatangan",
            'phone': "Nomor HP"
        }
        

