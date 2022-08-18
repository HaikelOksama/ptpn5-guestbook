
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
        model = Guest
        fields = '__all__'
        exclude = ['created']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Masukkan Nama Anda'
                }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Alamat Email Anda'
                }),
            'address': forms.Textarea(attrs={
               'placeholder': 'Alamat Tempat Tinggal Anda' 
            }),
            'reserve_time' : forms.DateTimeInput(attrs={
                'type':'datetime-local', 'min': stripped_time
                }),
            'phone' : forms.TextInput(attrs={
                'type' : 'number','placeholder': 'Berisi angka < 15 Digit'
                }),
            'needs': forms.Textarea(attrs={
                'placeholder': 'Jelaskan Keperluan Anda'
                }),
        }
        labels = {
            'name': "Nama",
            'email': "E-mail (opsional)",
            'address': "Alamat",
            'needs': "Keperluan",
            'reserve_time': "Jadwal Kedatangan",
            'phone': "Nomor HP"
        }
        

