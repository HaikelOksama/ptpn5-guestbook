
from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Guest
from .forms import GuestForms

from django.contrib import messages
from django.utils import timezone

from django.db.models import Q, Count #filter query chaining

from iteration_utilities import unique_everseen #Third Party Module to check if 
# Create your views here.

def guest_list_view(request):
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    d = request.GET.get('date') if request.GET.get('date') != None else '' 
    m = request.GET.get('month') if request.GET.get('month') != None else ''
    
    use_pagination = False
    now = datetime.now().strftime("%Y-%m")
    try:
        earliest = Guest.objects.order_by('reserve_time')[0]       
        early_date = earliest.reserve_time.strftime('%Y-%m-%d')
        early_month = earliest.reserve_time.strftime('%Y-%m') 
        
        print(early_date)
    except:
        early_date = None
        early_month = None
        
    print(request.GET)
    modelsQ = Guest.objects.all()
    
    if request.GET.get('search'):
        modelsQ = Guest.objects.filter(name__icontains = q)
        
    if request.GET.get('date'):
        # converted_date = models.DateTimeField().to_python(d)
        converted_date = datetime.strptime(d, "%Y-%m-%d")
        print(converted_date)
        modelsQ = Guest.objects.filter(
            reserve_time__day = converted_date.day,
            reserve_time__month = converted_date.month, 
            reserve_time__year = converted_date.year
            )
        
    if request.GET.get('month'):
        converted_date = datetime.strptime(m, "%Y-%m")
        modelsQ = Guest.objects.filter(reserve_time__month = converted_date.month, reserve_time__year = converted_date.year)

    # Paginator Stuff
    
    if modelsQ.count() > 20:
        use_pagination = True
        paginator = Paginator(modelsQ, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        of_pages = paginator.page_range
        context['range'] = of_pages
        context['page_obj'] = page_obj
    
    context  = {
        'current_month': now,
        'use_pagination' : use_pagination,
        'min_date': early_date, #CANNOT SEARCH IF DATE < EARLIEST OBJ DATE
        'min_month': early_month,
        'guest_list': modelsQ,
        'q': q,
        'd': d,
        'm': m,
    }
    if request.htmx:
        if request.method == 'POST':
            print(request.POST)
            instance = Guest.objects.get(id=request.POST['delete'])
            print(instance)
            instance.delete()
        return render(request, 'base/components/guest-table.html', context)
    
    return render(request, 'base/all_guest.html', context)

def home_view(request):
    try:
        oldObj = Guest.objects.order_by('reserve_time__year')[0]
        minYear = oldObj.reserve_time.strftime('%Y')
    except:
        minYear = None

    guest = Guest.objects.all().order_by('reserve_time')  
    day = []
    dayKey = []
    dailyData = []
    
    month = []
    monthKey = []
    monthlyData = []
    
    # x = Guest.objects.annotate(Count('reserve_time__month'))
    thisMonth = datetime.now().strftime('%m')
    
    
    year = datetime.now().strftime('%Y')
    now = datetime.now().strftime("%Y-%m")
       
    for count, obj in enumerate(guest):
        monthData = obj.get_month()
        dayData = obj.get_day()
        
        d = Guest.objects.filter(reserve_time__day = dayData, reserve_time__month = thisMonth, reserve_time__year = year).order_by('reserve_time__day').count()
        if d != 0:
            day.append({dayData: d})
            dayKey.append(dayData)
        
        a = Guest.objects.filter(reserve_time__month = monthData, reserve_time__year = year).order_by('reserve_time').count()
        # print(count)
        if a != 0:
            month.append({monthData: a})
            monthKey.append(monthData)
        
    # a = Guest.objects.filter(reserve_time__month = monthData, reserve_time__year = year).count()  
    day = list(unique_everseen(day))
    print(day)
    for xx,d in enumerate(day):
        for key in d.keys():
            if d.get(key) == 0:
                del day[xx]
        
        for data in d.values():
            if data != 0:
                dailyData.append(data)
    
    month = list(unique_everseen(month))#Remove duplicate month    
       
    #Get values data from list of dictionary [month].  
    for i,v in enumerate(month):
        for key in v.keys():           
            if v.get(key) == 0:              
                del month[i]
                            
        for val in v.values():
            if val != 0:
                monthlyData.append(val)
        # for val in v.keys():
    dayKey = list(unique_everseen(dayKey))
    print(dayKey)
    print(dailyData)
    
    monthKey = list(unique_everseen(monthKey))  
    monthKey = [str(x) for x in monthKey]
    monthlyData = [str(x) for x in monthlyData]
    
    for x in range(len(monthKey)):
        if monthKey[x] == '01':
            monthKey[x] = 'Januari'       
        if monthKey[x] == '02':
            monthKey[x] = 'Februari'
        if monthKey[x] == '03':
            monthKey[x] = 'Maret'
        if monthKey[x] == '04':
            monthKey[x] = 'April'
        if monthKey[x] == '05':
            monthKey[x] = 'May'
        if monthKey[x] == '06':
            monthKey[x] = 'Juni'
        if monthKey[x] == '07':
            monthKey[x] = 'July'
        if monthKey[x] == '08':
            monthKey[x] = 'Agustus'
        if monthKey[x] == '09':
            monthKey[x] = 'September'
        if monthKey[x] == '10':
            monthKey[x] = 'Oktober'
        if monthKey[x] == '11':
            monthKey[x] = 'November'
        if monthKey[x] == '12':
            monthKey[x] = 'Desember'
    
    context = {
        'guestList': guest,
        'now': now,
        'year': year,
        'thisMonth': thisMonth,
        'dayKey': dayKey,
        'dayData': dailyData,
        
        'allmonth': month,
        'monthKey': monthKey,
        'monthData': monthlyData,
    }
    return render(request, 'base/index.html', context)

def data_by_month(request):
    
   
    try:
        earliest = Guest.objects.order_by('reserve_time')[0] 
        early_month = earliest.reserve_time.strftime('%Y-%m')
        
        print(early_date)
    except:
        early_date = None
        early_month = None

    now = datetime.now().strftime("%Y-%m")
    print(now)
    m = request.GET.get('month') if request.GET.get('month') != None else ''
    
    # month_only = datetime.strptime(m, "%m")
    # year = datetime.strptime(m, "%Y") 
    converted_date = datetime.strptime(m, "%Y-%m") 
    
            
    if request.GET.get('month'):               
        modelsQ = Guest.objects.filter(reserve_time__month = converted_date.month, reserve_time__year = converted_date.year)
    
    modelsQ = Guest.objects.filter(reserve_time__month = converted_date.month, reserve_time__year = converted_date.year)
    
    info_message = f'Data Pada {m}'
    if m == now :
        info_message = 'Data Bulan Ini'
     
   
    
    context = {
        'min_month': early_month,
        'guest_list': modelsQ,
        'current_month': now,
        'info_message': info_message,
        

    }
    
    if request.htmx:
        return render(request, 'base/components/guest-table.html', context)
    
    return render(request,'base/monthly_data.html', context)
        
def monthly_data_view(request):
    day = []
    dayKey = []
    dailyData = []
    now = datetime.now().strftime("%Y-%m")
    guest = Guest.objects.all().order_by('reserve_time')   
    m = request.GET.get('month') if request.GET.get('month') != None else ''
    message = ''     
    try:
        earliest = Guest.objects.order_by('reserve_time')[0]       
        early_month = earliest.reserve_time.strftime('%Y-%m') 
        latest = Guest.objects.order_by('-reserve_time')[0]   
        latest_month = latest.reserve_time.strftime('%Y-%m') 
    except:
        early_month = None
        latest_month = None
    
    if 'month' in request.GET:
        try:
            converted_date = datetime.strptime(m, "%Y-%m")
            modelsQ = Guest.objects.filter(
            reserve_time__month = converted_date.month, 
            reserve_time__year = converted_date.year
            )
            
            month = converted_date.date()
            print(month)
            message = f'Data Pada Bulan {converted_date.month} ,Tahun {converted_date.year}'
            for count, obj in enumerate(modelsQ):
                dayData = obj.get_day()           
                d = Guest.objects.filter(reserve_time__day = dayData, reserve_time__month = converted_date.month, reserve_time__year = converted_date.year).order_by('reserve_time__day').count()
                if d != 0:
                    day.append({dayData: d})
                    dayKey.append(dayData)
            
            day = list(unique_everseen(day))
            dayKey = list(unique_everseen(dayKey))
            print(day)
                
            for xx,d in enumerate(day):
                for key in d.keys():
                    if d.get(key) == 0:
                        del day[xx]
                
                for data in d.values():
                    if data != 0:
                        dailyData.append(data)
                            
            print(f"Day key: {dayKey} | Day data: {dailyData}")   
        except:
            converted_date = now
            modelsQ = Guest.objects.none
            return redirect('monthly-data')
        
        if 'sort' in request.GET:
            sort = request.GET.get('sort')         
            # print(sort)
            if sort == 'name':
                modelsQ = modelsQ.order_by('-name')
            if sort == 'jadwalASC':
                modelsQ = modelsQ.order_by('reserve_time')   
            if sort == 'jadwalDESC':
                modelsQ = modelsQ.order_by('-reserve_time')  
        
                                  
    else:
        converted_date = now
        modelsQ = Guest.objects.none

    if request.method == 'POST': 
        if request.user.is_authenticated:     
            instanceId = request.POST['delete']           
            guest = Guest.objects.get(id=instanceId)
            # guest.delete()
            # return redirect('monthly-data')
            
    # Statistic Stuff   
    
      
    context = {
        'info_message': message,
        'guest_list': modelsQ,
        'min': early_month,
        'max': latest_month,
        'date': converted_date,
        'dayKey': dayKey,
        'dayData': dailyData,
    }
    
    if request.htmx:
        if request.method == 'POST':
            print(request.POST)
            instance = Guest.objects.get(id=request.POST['delete'])
            print(instance)
            instance.delete()
        return render(request, 'base/components/guest-table.html', context)

    # if request.htmx:
    #     print(request.htmx)
    #     if request.method == 'POST':
    #         print(request.POST)
    #         instance = Guest.objects.get(id=request.POST['delete'])
    #         print(instance)
    #         instance.delete()            
    #     # context['info_message'] = f'Data Pada Bulan {converted_date.month} ,Tahun {converted_date.year}'
    #     return render(request, 'base/components/guest-table.html', context)
    
    return render(request, 'base/monthly_data.html', context)

def delete_guest_view(request, pk):
    obj = Guest.objects.get(id=pk)
    if request.htmx:
        print(request.htmx)
    return HttpResponse('Success')

def new_guest_view(request):
    form = GuestForms()
    if request.method == 'POST':
        form = GuestForms(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.reserve_time < timezone.now():
                messages.error(request, 'Tanggal yang dimasukkan harus di masa mendatang')
            
            else:
                instance.save()
                messages.success(request, 'Success')
                return redirect('home')
    
    context = {
        'form' : form,
    }    
    
    return render(request, 'base/forms.html', context)
    
def statistic_view(request):
    try:
        oldObj = Guest.objects.order_by('reserve_time__year')[0]
        minYear = oldObj.reserve_time.strftime('%Y')
    except:
        minYear = None
    print(minYear)
    month = []
    monthKey = []
    monthlyData = []
    guest = Guest.objects.all().order_by('reserve_time')  
    # x = Guest.objects.annotate(Count('reserve_time__month'))
    if request.GET.get('year') != None:  
        year = request.GET.get('year')
    else:
        year = datetime.now().strftime('%Y')
    for count, obj in enumerate(guest):
        monthData = obj.get_month()
        a = Guest.objects.filter(reserve_time__month = monthData, reserve_time__year = year).order_by('reserve_time').count()
        # print(count)
        if a != 0:
            month.append({monthData: a})
            monthKey.append(monthData)
        
    # a = Guest.objects.filter(reserve_time__month = monthData, reserve_time__year = year).count()
        
    month = list(unique_everseen(month))#Remove duplicate month    
    
    #Get values data from list of dictionary [month]
    for x,v in enumerate(month):  
        print(v.values())
        for val in v.values():
            monthlyData.append(val)
    
    monthKey = list(unique_everseen(monthKey))
    
    monthKey = [str(x) for x in monthKey]
    monthlyData = [str(x) for x in monthlyData]
    
    print(monthKey[0])
    
    for x in range(len(monthKey)):
        if monthKey[x] == '01':
            monthKey[x] = 'Januari'       
        if monthKey[x] == '02':
            monthKey[x] = 'Februari'
        if monthKey[x] == '03':
            monthKey[x] = 'Maret'
        if monthKey[x] == '04':
            monthKey[x] = 'April'
        if monthKey[x] == '05':
            monthKey[x] = 'May'
        if monthKey[x] == '06':
            monthKey[x] = 'Juni'
        if monthKey[x] == '07':
            monthKey[x] = 'July'
        if monthKey[x] == '08':
            monthKey[x] = 'Agustus'
        if monthKey[x] == '09':
            monthKey[x] = 'September'
        if monthKey[x] == '10':
            monthKey[x] = 'Oktober'
        if monthKey[x] == '11':
            monthKey[x] = 'November'
        if monthKey[x] == '12':
            monthKey[x] = 'Desember'
    
    # print(month)
    # print(monthKey)
    # print(monthlyData)
    #TODO NEXT IS TO DISPLAY STATISTIC WITH CHART.JS WITH CORRESPONDING MONTH > VALUE 
    
    context = {
        'year': year,
        'allmonth': month,
        'monthKey': monthKey,
        'monthData': monthlyData,
    }
    
    return render(request, 'base/statistic.html', context)

