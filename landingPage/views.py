
from django.shortcuts import render, redirect
from base.forms import GuestForms
from django.contrib import messages
from django.contrib.messages import get_messages
# Create your views here.

def new_guest_view(request):
    done = False   
    form = GuestForms()
    if request.method == 'POST':
        form = GuestForms(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.save()
            print(instance.name)
            messages.success(request, f'{instance.name} Telah Berhasil Ditambahkan')
  
            return redirect('guest')
    context = {
        'form' : form,
        'success' : done
    }    
    
    return render(request, 'index.html', context)
