from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from .models import Profile, Stations, Trains, Choices, SatTrains, SunTrains, MonTrains, TueTrains, WedTrains, ThuTrains, FriTrains, Tickets
from datetime import date
import datetime
import string
from random import sample, choice
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    obj = (list(Stations.objects.all()))
    obj2= (list(Choices.objects.all()))
    x = datetime.date.today()
    y = datetime.timedelta(days = 6)
    z = x + y
    print(x)
    print(y)
    print(z)
    context = {
        'objects' : obj,
        'cobjects': obj2,
        'min' : x,
        'max' : z
    }
    return render(request,  "home.html", context )

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def register(request):
    #chose = Profile.gender_choice()
    if request.user.is_authenticated:
        messages.info(request, 'Already Loged in', extra_tags = "logedin")
        return redirect('/')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name'] 
            last_name = request.POST['last_name']
            email = request.POST['email']
            mobile = request.POST['mobile2']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            gender = request.POST['gender']

            if password1 == password2:
                if Profile.objects.filter(email = email ).exists():
                    messages.error(request, 'Email already used', extra_tags = "usedmail")
                    return redirect('/register')
                else:
                    chars = string.digits
                    length = 6
                    active_code = ''.join(choice(chars) for _ in range(length))
                    user = Profile.objects.create_user(first_name = first_name,
                        last_name = last_name,
                        email = email,
                        password = password1,
                        mobile = mobile,
                        gender = gender,
                        active_code = active_code
                    )
                    user.is_active = False
                    user.save()

                    template = render_to_string('email.html', {'name' : user.first_name, 'code' : active_code})
                    email = EmailMessage(
                        'Account activation code.',
                        template,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                    )
                    email.fail_silently = False
                    email.send()
                    messages.info(request, 'Please check your email for activation code', extra_tags = "code")
                    return redirect('/activation')
            else:
                messages.error(request, 'Passwords did not match', extra_tags = "mispas")
                return redirect('/register')
        else:
            return render(request,"register.html")

def activation(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Account already activated', extra_tags = "activated")
        return redirect('/')
    
    else:
        if request.method == 'POST':
            email = request.POST['email']
            code = request.POST['code']

            if Profile.objects.filter(email = email ).exists():

                user = Profile.objects.get(email = email )
                usera = Profile.objects.filter(email = email )

                if user.active_code == code:
                    usera.update(is_active = True)
                    messages.success(request, 'Account activated.', extra_tags = "activated")
                    return redirect('/login')
                else:
                    messages.error(request, 'Wrong code.', extra_tags = "activated")
                    return redirect('/activation')
            else:
                messages.error(request, 'Wrong email.', extra_tags = "activated")
                return redirect('/activation')
        else:
            return render(request,"activation.html")

def login(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already loged in', extra_tags = "logedin")
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            usera = Profile.objects.get(email = email)

            user = auth.authenticate(email = email, password = password)

            if usera.is_active == True:
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, 'Welcome'+' '+usera.first_name+' '+usera.last_name, extra_tags = "login")
                    return redirect('/')
                else:
                    messages.error(request, 'Wrong email or password', extra_tags = "login")
                    return redirect('/login')

            else:
                messages.error(request, 'Please active your account first', extra_tags = "activated")
                return redirect('/activation')

        else:
            return render(request,"login.html")

def logout(request):
    auth.logout(request)
    messages.info(request, 'Loged out', extra_tags = "login")
    return redirect('/')

def profiling(request):
    if request.user.is_authenticated:
        return render(request,"profile.html")
    else:
        return redirect('/login')

def recover(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Logout First.',  extra_tags = "logedin")
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.POST['email']

            if Profile.objects.filter(email = email ).exists():
                
                user = Profile.objects.get(email = email )
                usera = Profile.objects.filter(email = email )
                chars = string.digits
                length = 6
                reset_code = ''.join(choice(chars) for _ in range(length))
                usera.update(reset_code = reset_code)

                template = render_to_string('passres.html', {'name' : user.first_name, 'code' : reset_code})
                email = EmailMessage(
                    'Password reset code.',
                    template,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email.fail_silently = False
                email.send()
                messages.info(request, 'Please check your email for reset code.',  extra_tags = "respas")
                return redirect('/recover_final')
            else:
                messages.error(request, 'Wrong email address.',  extra_tags = "respas")
                return redirect('/recover')

        else:
            return render(request,"recover.html")

def recover_final(request):
    if request.method == 'POST':
        email     = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        code      = request.POST['code']

        if password1 == password2:
            if Profile.objects.filter(email = email ).exists():
                user = Profile.objects.get(email = email )

                if user.reset_code == code:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'New password set', extra_tags = "respas" )
                    return redirect('/login')

                else:
                    messages.error(request, 'Wrong code', extra_tags = "respas")
                    return redirect('/recover_final')
            else:
                messages.error(request, 'User not registered', extra_tags = "respas")
                return redirect('/recover_final')
    
        else:
            messages.error(request, 'Password did not match!', extra_tags = "respas")
            return redirect('/recover_final')

    else:
        return render(request,"recover_final.html")

def maintain(request):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            return render(request,"maintain.html")
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def stations(request):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            if request.method == "POST":
                station_name = request.POST['station_name']
                factor      = request.POST['factors']
                station_id  = request.POST['station_id']
                station      = Stations(
                    station_name = station_name,
                    factors = factor,
                    station_id = station_id
                )
                station.save()
                messages.success(request, 'New station added.', extra_tags = "respas")
                return redirect('/stations')
            else:
                return render(request,"stations.html")
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def station_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            obj = (list(Stations.objects.all())) 
            context = {
                'objects' : obj
            }
            return render(request,"station_view.html", context)
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def trains(request):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            if request.method == "POST":
                train_name  = request.POST['train_name']
                factor      = request.POST['factors']
                train_id    = request.POST['train_id']
                stopages    = request.POST.getlist('stopages')
                deptim      = request.POST['deptim']
                offday      = request.POST['offday']
                ac_b_seat    = request.POST['ac_b_seat']
                ac_s_seat    = request.POST['ac_s_seat']
                f_b_seat     = request.POST['f_b_seat']
                f_s_seat     = request.POST['f_s_seat']
                snigdha_seat = request.POST['snigdha_seat']
                s_chair_seat = request.POST['s_chair_seat']
                sulov_seat   = request.POST['sulov_seat']
                total       = int(ac_b_seat) + int(ac_s_seat) + int(f_b_seat) + int(f_s_seat) + int(snigdha_seat) + int(s_chair_seat) + int(sulov_seat) 
                train       = Trains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                sattrain       = SatTrains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                suntrain       = SunTrains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                montrain       = MonTrains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                tuetrain       = TueTrains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                wedtrain       = WedTrains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                thutrain       = ThuTrains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                fritrain       = FriTrains(
                    train_name = train_name, 
                    factors = factor, 
                    train_id = train_id, 
                    stopages = stopages, 
                    departure_time = deptim, 
                    offday = offday, 
                    ac_b_seat = ac_b_seat, 
                    ac_s_seat = ac_s_seat,
                    f_b_seat = f_b_seat,
                    f_s_seat = f_s_seat,
                    snigdha_seat = snigdha_seat,
                    s_chair_seat = s_chair_seat,
                    sulov_seat = sulov_seat,
                    total = total
                )
                train.save()
                sattrain.save()
                suntrain.save()
                montrain.save()
                tuetrain.save()
                wedtrain.save()
                thutrain.save()
                fritrain.save()
                print(total)
                #train.stopages.set(stopages)
                obj = (list(Stations.objects.all())) 
                context = {
                    'objects' : obj
                }
                messages.success(request, 'New train added.', extra_tags = "respas")
                return redirect('/trains', context)
            else:
                obj = (list(Stations.objects.all())) 
                context = {
                    'objects' : obj
                }
                return render(request,"trains.html", context)
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def train_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            #j = 1
            #obj = Stations.objects.get(pk = j)
            obj = (list(Trains.objects.all()))
            for train in obj:
                print(train.total)
            context = {
                'objects' : obj
            }
            return render(request,"train_view.html", context)
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def delete(request, train_id):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            obj  = Trains.objects.get(train_id = train_id)
            obj1 = SatTrains.objects.get(train_id = train_id)
            obj2 = SunTrains.objects.get(train_id = train_id)
            obj3 = MonTrains.objects.get(train_id = train_id)
            obj4 = TueTrains.objects.get(train_id = train_id)
            obj5 = WedTrains.objects.get(train_id = train_id)
            obj6 = ThuTrains.objects.get(train_id = train_id)
            obj7 = FriTrains.objects.get(train_id = train_id)
            obj.delete()
            obj1.delete()
            obj2.delete()
            obj3.delete()
            obj4.delete()
            obj5.delete()
            obj6.delete()
            obj7.delete()
            messages.success(request, 'Train deleted successfully', extra_tags = "respas")
            return redirect('/train_view')
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def edit(request, train_id):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            train_obj = Trains.objects.get(train_id = train_id)
            station_obj = (list(Stations.objects.all()))
            return render(request, 'edit.html', {'objects':train_obj, 'objects2':station_obj} )
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def update(request):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            if request.method == "POST":
                #stopages     = request.POST.getlist('stopages')
                train_id     = request.POST['trains_id']
                deptim       = request.POST['deptim']
                #offday       = request.POST['offday']
                ac_b_seat    = request.POST['ac_b_seat']
                ac_s_seat    = request.POST['ac_s_seat']
                f_b_seat     = request.POST['f_b_seat']
                f_s_seat     = request.POST['f_s_seat']
                snigdha_seat = request.POST['snigdha_seat']
                s_chair_seat = request.POST['s_chair_seat']
                sulov_seat   = request.POST['sulov_seat']
                total        = int(ac_b_seat) + int(ac_s_seat) + int(f_b_seat) + int(f_s_seat) + int(snigdha_seat) + int(s_chair_seat) + int(sulov_seat)
                train = Trains.objects.filter(train_id = train_id)
                train1 = SatTrains.objects.filter(train_id = train_id)
                train2 = SunTrains.objects.filter(train_id = train_id)
                train3 = MonTrains.objects.filter(train_id = train_id)
                train4 = ThuTrains.objects.filter(train_id = train_id)
                train5 = WedTrains.objects.filter(train_id = train_id)
                train6 = TueTrains.objects.filter(train_id = train_id)
                train7 = FriTrains.objects.filter(train_id = train_id)

                train.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                train1.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                train2.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                train3.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                train4.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                train5.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                train6.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                train7.update(
                    #stopages        = stopages, 
                    departure_time  = deptim, 
                    #offday          = offday,
                    ac_b_seat       = ac_b_seat, 
                    ac_s_seat       = ac_s_seat,
                    f_b_seat        = f_b_seat,
                    f_s_seat        = f_s_seat,
                    snigdha_seat    = snigdha_seat,
                    s_chair_seat    = s_chair_seat,
                    sulov_seat      = sulov_seat,
                    total           = total
                )
                messages.success(request, 'Informations Updated', extra_tags = "respas")
                return redirect('/train_view')
        else:
            messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'You do not have admin privilage.', extra_tags = "respas")
        return redirect('/')

def selection(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            station     = Stations.objects.all()
            frome       = request.POST['from']
            to          = request.POST['to']
            adult       = request.POST['adult']
            child       = request.POST['child']
            datt        = request.POST['date']
            classes     = request.POST['classes']
            print(child)
            dt = datetime.datetime.strptime(datt, '%Y-%m-%d')
            date =  ('{0}, {1}, {2}'.format( dt.year, dt.month, dt.day))
            x = datetime.datetime(dt.year, dt.month, dt.day)
            y = (x.strftime("%A"))
            #print(date.strftime("%A"))
            print(y)
            #print(date)
            for s in station:
                if s.station_name == frome:
                    f = s.factors
                if s.station_name == to:
                    t = s.factors
            #c = child/2
            #print(frome, "  ", to)
            if y == 'Saturday':
                train       = SatTrains.objects.all()
                #print("1")
            elif y == 'Sunday':
                train       = SunTrains.objects.all()
                #print("2")
            elif y == 'Monday':
                train       = MonTrains.objects.all()
                #print("3")
            elif y == 'Tuesday':
                train       = TueTrains.objects.all()
                #print("4")
            elif y == 'Wednesday':
                train       = WedTrains.objects.all()
                #print("5")
            elif y == 'Thursday':
                train       = ThuTrains.objects.all()
                #print("6")
            elif y == 'Friday':
                train       = FriTrains.objects.all()
                #print("7")

            if frome != to :
                seat = int(adult) + int(child)
                if seat < 5:
                    train = train.filter(stopages__icontains = frome)
                    train = train.filter(stopages__icontains = to)
                    for t in train:
                        if t.total < seat:
                            train = train.exclude(train_id = t.train_id)
                        if t.offday == y:
                            train = train.exclude(offday = y)

                        if classes == 'ac_b_seat':
                            if t.ac_b_seat < seat:
                                train = train.exclude(train_id = t.train_id)
                        elif classes == 'ac_s_seat':
                            if t.ac_s_seat < seat:
                                train = train.exclude(train_id = t.train_id)
                        elif classes == 'f_b_seat':
                            if t.f_b_seat < seat:
                                train = train.exclude(train_id = t.train_id)
                        elif classes == 'f_s_seat':
                            if t.f_s_seat < seat:
                                train = train.exclude(train_id = t.train_id)
                        elif classes == 'snigdha_seat':
                            if t.snigdha_seat < seat:
                                train = train.exclude(train_id = t.train_id)
                        elif classes == 's_chair_seat':
                            if t.s_chair_seat < seat:
                                train = train.exclude(train_id = t.train_id)
                        elif classes == 'sulov_seat':
                            if t.sulov_seat < seat:
                                train = train.exclude(train_id = t.train_id)
                        else:
                            messages.error(request, 'Invalid Class Choice!')
                    
                    print(classes)
                    context = {
                        'objects' : train,
                        'classes' : classes,
                        'adult'   : adult,
                        'child'   : child,
                        'frome'   : frome,
                        'to'      : to,
                        'date'    : datt,
                        'day'     : y
                    }
                    return render(request, "selection.html", context)
                else:
                    messages.error(request, 'Selected seats are more than 4!', extra_tags = "respas")
                    return redirect("/")
            else:
                messages.error(request, 'Invalid Locations!', extra_tags = "respas")
                return redirect("/")
        else:
            messages.warning(request, 'You are not loged in', extra_tags = "respas")
            return redirect('/')
    else:
        messages.error(request, 'Not enough travel informations', extra_tags = "respas")
        return redirect('/')

def confirm(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            #train_id = request.POST['train_id']
            station     = Stations.objects.all()
            date        = request.POST['date']
            day         = request.POST['day']
            train_name  = request.POST['train_name']
            train_id    = request.POST['train_id']
            frome       = request.POST['frome']
            to          = request.POST['to']
            classes     = request.POST['classes']
            adult       = request.POST['adltst']
            child       = request.POST['chldst']
            deptim      = request.POST['deptim']
            user_id     = request.user.id
            fname       = request.user.first_name
            lname       = request.user.last_name
            email       = request.user.email
            mobile      = request.user.mobile
            train       = Trains.objects.get(train_id = train_id)
            
            for s in station:
                if s.station_name == frome:
                    f = s.factors
                if s.station_name == to:
                    t = s.factors
            fact = abs(f - t)*10
            print(fact, train.factors, fact/train.factors)
            jt = datetime.time((fact/train.factors))
            dt = train.departure_time
            z = datetime.timedelta(hours = jt.hour, minutes=jt.minute)
            at =((datetime.datetime.combine(datetime.date(1,1,1),dt) + z).time())
            if classes == 'AC Barth':
                seat_factor = 7
            elif classes == 'AC Seat':
                seat_factor = 10.5
            elif classes == 'First Claass Barth':
                seat_factor = 12
            elif classes == 'First Class Seat':
                seat_factor = 14
            elif classes == 'Snigdha':
                seat_factor = 15
            elif classes == 'Sovon Seat':
                seat_factor = 19
            elif classes == 'Sulov Seat':
                seat_factor = 23
            chld = '{:.2f}'.format((int(child)*8.4)/10)
            sfair = float('{:.2f}'.format((float(train.factors)/(seat_factor))*float(fact)))
            seat = int(adult) + float(chld)
            seat = float('{:.2f}'.format(seat))
            fair = (sfair*seat)/10
            fair = float('{:.2f}'.format(fair))
            charge = 20*(int(adult)+int(child))
            total = fair + charge
            total = float('{:.2f}'.format(total))
            print(fair)
            context = {
                'date'          : date,
                'day'           : day,
                'train_name'    : train_name,
                'train_id'      : train_id,
                'frome'         : frome,
                'to'            : to,
                'classes'       : classes,
                'adult'         : adult,
                'child'         : child,
                'deptim'        : deptim,
                'at'            : at,
                'user_id'       : user_id,
                'fname'         : fname,
                'lname'         : lname,
                'email'         : email,
                'mobile'        : mobile,
                'fair'          : fair,
                'charge'        : charge,
                'total'         : total,
            }
            return render(request, 'confirm.html', context)
        # if request.method == "POST":
        #     train_id = request.POST['train_id']
        #     print(train_id)
        #     return render(request, 'addi.html')
            
        else:
            return redirect('/search')
    else:
        messages.error(request, 'You are not loged in', extra_tags = "respas")
        return redirect('/')

def search(request):
    train       = Trains.objects.all()
    frome       = "N/A"
    to          = "N/A"
    date        = "N/A"
    day         = "N/A"
    adult       = "N/A"
    child       = "N/A"
    if frome != to:
        train = train.filter(stopages__icontains = frome)
        train = train.filter(stopages__icontains = to)
    else:
        messages.error(request, "invalid Locations!")
    context = {
                    'objects' : train, 'date' : date, 'day' : day, 'frome' : frome, 'to' : to, 'adult' : adult, 'child' : child
                }
    return render(request, "selection.html", context)

def verification(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            date        = request.POST['date']
            day         = request.POST['day']
            train_name  = request.POST['train_name']
            train_id    = request.POST['train_id']
            frome       = request.POST['frome']
            to          = request.POST['to']
            classes     = request.POST['classes']
            adult       = request.POST['adult']
            child       = request.POST['child']
            deptim      = request.POST['deptim']
            at          = request.POST['at']
            user_id     = request.POST['user_id']
            name        = request.POST['buyer_name']
            email       = request.POST['email']
            mobile      = request.POST['mobile']
            fair        = request.POST['fair']
            charge      = request.POST['charge']
            total       = request.POST['total']

            chars = string.ascii_letters + string.digits
            length = 8
            verify_code = ''.join(choice(chars) for _ in range(length))
            print(verify_code)
            tickets = Tickets(
                date = date,
                day = day,
                verify_code = verify_code,
                train_name = train_name,
                train_id = train_id,
                frome = frome,
                to = to,
                classes = classes,
                adult = adult,
                child = child,
                departure_time = deptim,
                arrival_time = at,
                buyer_id = user_id,
                buyer_name = name,
                email = email,
                mobile = mobile,
                fair = fair,
                charge = charge,
                total = total,
            )
            tickets.save()
            return HttpResponseRedirect("verification")
        else:
            user_id = request.user.id
            #return render(request, 'tickets.html')
            #if Profile.objects.filter(username = username ).exists():
            if Tickets.objects.filter(buyer_id = user_id ).exists():
                ticket = Tickets.objects.filter(buyer_id = user_id, status = "Unverified")
                #ticket = Tickets.objects.filter(status = "Unverified")
                for t in ticket:
                    print(t)
                context = {
                    'tickets' : ticket
                }
                return render(request, 'verify.html', context)
            else:
                messages.info(request, 'No purchase history!')
                return render(request, 'verify.html')
            #return render(request, 'purchase.html')
    else:
        return redirect('/login')

def verify(request):
    if request.method == "POST":
        ticket_id       = request.POST['invoice_no']
        verify_code     = request.POST['verify_code']
        day             = request.POST['day']
        train_id        = int(request.POST['train_id'])
        classes         = request.POST['classes']
        adult           = request.POST['adult']
        child           = request.POST['child']

        seat = int(adult) + int(child)

        ticket = Tickets.objects.get(ticket_id = ticket_id)
        if verify_code == ticket.verify_code:
            Tickets.objects.filter(ticket_id = ticket_id).update(
                status = 'Verified'
            )
        else:
            messages.error(request, 'Invalid Code!')
        
        if day == 'Saturday':
            if classes   == 'AC Barth':
                train = SatTrains.objects.get(train_id = train_id)
                new = train.ac_b_seat - seat
                SatTrains.objects.filter(train_id = train_id).update(
                    ac_b_seat = new
                )
            elif classes == 'AC Seat':
                train = SatTrains.objects.get(train_id = train_id)
                new = train.ac_s_seat - seat
                SatTrains.objects.filter(train_id = train_id).update(
                    ac_s_seat = new
                )
            elif classes == 'First Claass Barth':
                train = SatTrains.objects.get(train_id = train_id)
                new = train.f_b_seat - seat
                SatTrains.objects.filter(train_id = train_id).update(
                    f_b_seat = new
                )
                pass
            elif classes == 'First Class Seat':
                train = SatTrains.objects.get(train_id = train_id)
                new = train.f_s_seat - seat
                SatTrains.objects.filter(train_id = train_id).update(
                    f_s_seat = new
                )
            elif classes == 'Snigdha':
                train = SatTrains.objects.get(train_id = train_id)
                new = train.snigdha_seat - seat
                SatTrains.objects.filter(train_id = train_id).update(
                    snigdha_seat = new
                )
                pass
            elif classes == 'Sovon Seat':
                train = SatTrains.objects.get(train_id = train_id)
                new = train.s_chair_seat - seat
                SatTrains.objects.filter(train_id = train_id).update(
                    s_chair_seat = new
                )
            elif classes == 'Sulov Seat':
                train = SatTrains.objects.get(train_id = train_id)
                new = train.sulov_seat - seat
                SatTrains.objects.filter(train_id = train_id).update(
                    sulov_seat = new
                )
        elif day == 'Sunday':
            if classes   == 'AC Barth':
                train = SunTrains.objects.get(train_id = train_id)
                new = train.ac_b_seat - seat
                SunTrains.objects.filter(train_id = train_id).update(
                    ac_b_seat = new
                )
            elif classes == 'AC Seat':
                train = SunTrains.objects.get(train_id = train_id)
                new = train.ac_s_seat - seat
                SunTrains.objects.filter(train_id = train_id).update(
                    ac_s_seat = new
                )
            elif classes == 'First Claass Barth':
                train = SunTrains.objects.get(train_id = train_id)
                new = train.f_b_seat - seat
                SunTrains.objects.filter(train_id = train_id).update(
                    f_b_seat = new
                )
                pass
            elif classes == 'First Class Seat':
                train = SunTrains.objects.get(train_id = train_id)
                new = train.f_s_seat - seat
                SunTrains.objects.filter(train_id = train_id).update(
                    f_s_seat = new
                )
            elif classes == 'Snigdha':
                train = SunTrains.objects.get(train_id = train_id)
                new = train.snigdha_seat - seat
                SunTrains.objects.filter(train_id = train_id).update(
                    snigdha_seat = new
                )
                pass
            elif classes == 'Sovon Seat':
                train = SunTrains.objects.get(train_id = train_id)
                new = train.s_chair_seat - seat
                SunTrains.objects.filter(train_id = train_id).update(
                    s_chair_seat = new
                )
            elif classes == 'Sulov Seat':
                train = SunTrains.objects.get(train_id = train_id)
                new = train.sulov_seat - seat
                SunTrains.objects.filter(train_id = train_id).update(
                    sulov_seat = new
                )
        elif day == 'Monday':
            if classes   == 'AC Barth':
                train = MonTrains.objects.get(train_id = train_id)
                new = train.ac_b_seat - seat
                MonTrains.objects.filter(train_id = train_id).update(
                    ac_b_seat = new
                )
            elif classes == 'AC Seat':
                train = MonTrains.objects.get(train_id = train_id)
                new = train.ac_s_seat - seat
                MonTrains.objects.filter(train_id = train_id).update(
                    ac_s_seat = new
                )
            elif classes == 'First Claass Barth':
                train = MonTrains.objects.get(train_id = train_id)
                new = train.f_b_seat - seat
                MonTrains.objects.filter(train_id = train_id).update(
                    f_b_seat = new
                )
                pass
            elif classes == 'First Class Seat':
                train = MonTrains.objects.get(train_id = train_id)
                new = train.f_s_seat - seat
                MonTrains.objects.filter(train_id = train_id).update(
                    f_s_seat = new
                )
            elif classes == 'Snigdha':
                train = MonTrains.objects.get(train_id = train_id)
                new = train.snigdha_seat - seat
                MonTrains.objects.filter(train_id = train_id).update(
                    snigdha_seat = new
                )
                pass
            elif classes == 'Sovon Seat':
                train = MonTrains.objects.get(train_id = train_id)
                new = train.s_chair_seat - seat
                MonTrains.objects.filter(train_id = train_id).update(
                    s_chair_seat = new
                )
            elif classes == 'Sulov Seat':
                train = MonTrains.objects.get(train_id = train_id)
                new = train.sulov_seat - seat
                MonTrains.objects.filter(train_id = train_id).update(
                    sulov_seat = new
                )
        elif day == 'Tuesday':
            if classes   == 'AC Barth':
                train = TueTrains.objects.get(train_id = train_id)
                new = train.ac_b_seat - seat
                TueTrains.objects.filter(train_id = train_id).update(
                    ac_b_seat = new
                )
            elif classes == 'AC Seat':
                train = TueTrains.objects.get(train_id = train_id)
                new = train.ac_s_seat - seat
                TueTrains.objects.filter(train_id = train_id).update(
                    ac_s_seat = new
                )
            elif classes == 'First Claass Barth':
                train = TueTrains.objects.get(train_id = train_id)
                new = train.f_b_seat - seat
                TueTrains.objects.filter(train_id = train_id).update(
                    f_b_seat = new
                )
                pass
            elif classes == 'First Class Seat':
                train = TueTrains.objects.get(train_id = train_id)
                new = train.f_s_seat - seat
                TueTrains.objects.filter(train_id = train_id).update(
                    f_s_seat = new
                )
            elif classes == 'Snigdha':
                train = TueTrains.objects.get(train_id = train_id)
                new = train.snigdha_seat - seat
                TueTrains.objects.filter(train_id = train_id).update(
                    snigdha_seat = new
                )
                pass
            elif classes == 'Sovon Seat':
                train = TueTrains.objects.get(train_id = train_id)
                new = train.s_chair_seat - seat
                TueTrains.objects.filter(train_id = train_id).update(
                    s_chair_seat = new
                )
            elif classes == 'Sulov Seat':
                train = TueTrains.objects.get(train_id = train_id)
                new = train.sulov_seat - seat
                TueTrains.objects.filter(train_id = train_id).update(
                    sulov_seat = new
                )
        elif day == 'Wednesday':
            if classes   == 'AC Barth':
                train = WedTrains.objects.get(train_id = train_id)
                new = train.ac_b_seat - seat
                WedTrains.objects.filter(train_id = train_id).update(
                    ac_b_seat = new
                )
            elif classes == 'AC Seat':
                train = WedTrains.objects.get(train_id = train_id)
                new = train.ac_s_seat - seat
                WedTrains.objects.filter(train_id = train_id).update(
                    ac_s_seat = new
                )
            elif classes == 'First Claass Barth':
                train = WedTrains.objects.get(train_id = train_id)
                new = train.f_b_seat - seat
                WedTrains.objects.filter(train_id = train_id).update(
                    f_b_seat = new
                )
                pass
            elif classes == 'First Class Seat':
                train = WedTrains.objects.get(train_id = train_id)
                new = train.f_s_seat - seat
                WedTrains.objects.filter(train_id = train_id).update(
                    f_s_seat = new
                )
            elif classes == 'Snigdha':
                train = WedTrains.objects.get(train_id = train_id)
                new = train.snigdha_seat - seat
                WedTrains.objects.filter(train_id = train_id).update(
                    snigdha_seat = new
                )
                pass
            elif classes == 'Sovon Seat':
                train = WedTrains.objects.get(train_id = train_id)
                new = train.s_chair_seat - seat
                WedTrains.objects.filter(train_id = train_id).update(
                    s_chair_seat = new
                )
            elif classes == 'Sulov Seat':
                train = WedTrains.objects.get(train_id = train_id)
                new = train.sulov_seat - seat
                WedTrains.objects.filter(train_id = train_id).update(
                    sulov_seat = new
                )
        elif day == 'Thursday':
            if classes   == 'AC Barth':
                train = ThuTrains.objects.get(train_id = train_id)
                new = train.ac_b_seat - seat
                ThuTrains.objects.filter(train_id = train_id).update(
                    ac_b_seat = new
                )
            elif classes == 'AC Seat':
                train = ThuTrains.objects.get(train_id = train_id)
                new = train.ac_s_seat - seat
                ThuTrains.objects.filter(train_id = train_id).update(
                    ac_s_seat = new
                )
            elif classes == 'First Claass Barth':
                train = ThuTrains.objects.get(train_id = train_id)
                new = train.f_b_seat - seat
                ThuTrains.objects.filter(train_id = train_id).update(
                    f_b_seat = new
                )
                pass
            elif classes == 'First Class Seat':
                train = ThuTrains.objects.get(train_id = train_id)
                new = train.f_s_seat - seat
                ThuTrains.objects.filter(train_id = train_id).update(
                    f_s_seat = new
                )
            elif classes == 'Snigdha':
                train = ThuTrains.objects.get(train_id = train_id)
                new = train.snigdha_seat - seat
                ThuTrains.objects.filter(train_id = train_id).update(
                    snigdha_seat = new
                )
                pass
            elif classes == 'Sovon Seat':
                train = ThuTrains.objects.get(train_id = train_id)
                new = train.s_chair_seat - seat
                ThuTrains.objects.filter(train_id = train_id).update(
                    s_chair_seat = new
                )
            elif classes == 'Sulov Seat':
                train = ThuTrains.objects.get(train_id = train_id)
                new = train.sulov_seat - seat
                ThuTrains.objects.filter(train_id = train_id).update(
                    sulov_seat = new
                )
        elif day == 'Friday':
            if classes   == 'AC Barth':
                train = FriTrains.objects.get(train_id = train_id)
                new = train.ac_b_seat - seat
                FriTrains.objects.filter(train_id = train_id).update(
                    ac_b_seat = new
                )
            elif classes == 'AC Seat':
                train = FriTrains.objects.get(train_id = train_id)
                new = train.ac_s_seat - seat
                FriTrains.objects.filter(train_id = train_id).update(
                    ac_s_seat = new
                )
            elif classes == 'First Claass Barth':
                train = FriTrains.objects.get(train_id = train_id)
                new = train.f_b_seat - seat
                FriTrains.objects.filter(train_id = train_id).update(
                    f_b_seat = new
                )
                pass
            elif classes == 'First Class Seat':
                train = FriTrains.objects.get(train_id = train_id)
                new = train.f_s_seat - seat
                FriTrains.objects.filter(train_id = train_id).update(
                    f_s_seat = new
                )
            elif classes == 'Snigdha':
                train = FriTrains.objects.get(train_id = train_id)
                new = train.snigdha_seat - seat
                FriTrains.objects.filter(train_id = train_id).update(
                    snigdha_seat = new
                )
                pass
            elif classes == 'Sovon Seat':
                train = FriTrains.objects.get(train_id = train_id)
                new = train.s_chair_seat - seat
                FriTrains.objects.filter(train_id = train_id).update(
                    s_chair_seat = new
                )
            elif classes == 'Sulov Seat':
                train = FriTrains.objects.get(train_id = train_id)
                new = train.sulov_seat - seat
                FriTrains.objects.filter(train_id = train_id).update(
                    sulov_seat = new
                )

        # if classes   == 'AC Barth':
        # elif classes == 'AC Seat':
        # elif classes == 'First Claass Barth':
        # elif classes == 'First Class Seat':
        # elif classes == 'Snigdha':
        # elif classes == 'Sovon Seat':
        # elif classes == 'Sulov Seat':
            
        return redirect('/verification')
    else:
        return redirect('/verification')

def tickets(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        #return render(request, 'tickets.html')
        #if Profile.objects.filter(username = username ).exists():
        if Tickets.objects.filter(buyer_id = user_id ).exists():
            ticket = Tickets.objects.filter(buyer_id = user_id, status = "Verified")
            #ticket = Tickets.objects.filter(status = "Verified")
            context = {
                'tickets' : ticket
            }
            return render(request, 'tickets(0).html', context)
        else:
            messages.error(request, 'No purchase history!')
            return render(request, 'tickets.html')
    else:
        return redirect('/login')

def reset(request):
    if request.user.is_authenticated:
        if request.user.is_admin == True:
            if request.method == 'POST':
                day = request.POST['day']
                if day == 'saturday':
                    train       = SatTrains.objects.all()
                    #print("1")
                elif day == 'sunday':
                    train       = SunTrains.objects.all()
                    #print("2")
                elif day == 'monday':
                    train       = MonTrains.objects.all()
                    #print("3")
                elif day == 'tuesday':
                    train       = TueTrains.objects.all()
                    #print("4")
                elif day == 'wednesday':
                    train       = WedTrains.objects.all()
                    #print("5")
                elif day == 'thursday':
                    train       = ThuTrains.objects.all()
                    #print("6")
                elif day == 'friday':
                    train       = FriTrains.objects.all()
                    #print("7")
                
                #main_train = Trains.objects.all()

                for t in train:
                    mtrain = Trains.objects.get(train_id = t.train_id)
                    total = (mtrain.ac_b_seat + mtrain.ac_s_seat + mtrain.f_b_seat + mtrain.f_s_seat + mtrain.snigdha_seat + mtrain.s_chair_seat + mtrain.sulov_seat)
                    train.filter(train_id = t.train_id).update(
                        ac_b_seat    = mtrain.ac_b_seat,
                        ac_s_seat    = mtrain.ac_s_seat,
                        f_b_seat     = mtrain.f_b_seat,
                        f_s_seat     = mtrain.f_s_seat,
                        snigdha_seat = mtrain.snigdha_seat,
                        s_chair_seat = mtrain.s_chair_seat,
                        sulov_seat   = mtrain.sulov_seat,
                        total        = total
                    )
                return render(request, 'reset.html')
            else:
                return render(request, 'reset.html')
        else:
            return redirect('/login')
    else:
        return redirect('/login')