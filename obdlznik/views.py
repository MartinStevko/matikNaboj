from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect

from django.utils import timezone
from random import randint, choice

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *

def error_404(request):
    template = 'obdlznik/error.html'
    return render(request, template, {'number':404})

def error_500(request):
    template = 'obdlznik/error.html'
    return render(request, template, {'number':500})

def log_in(request):
    template = 'obdlznik/login.html'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/obdlznik/')
        else:
            message = 'Zadané používateľské meno alebo heslo je neprávne!'
            error = username + ' (' + password + ') - ' + message
            Message.objects.create(text=error, importance=True)
            return render(request, template, {'message':message})

    else:
        return render(request, template, {})

def logout_page(request):
    template = 'obdlznik/logout.html'
    return render(request, template, {})

def log_out(request):
    logout(request)
    return redirect('/obdlznik/')

def index(request):
    template = 'obdlznik/index.html'
    return render(request, template, {})

def druzinka(request):
    template = 'obdlznik/druzinka.html'
    druzinka = Druzinka.objects.get(idUser=request.User)

    if request.method == 'POST':
        if 'move' in request.POST:
            if request.POST['x']!=druzinka.me_x and request.POST['y']!=druzinka.me_y:
                message = 'Posun je možný iba po jednej osi, nie oboch!'
                error = str(druzinka.nazov) + ' - ' + message
                Message.objects.create(text=error)
                return render(request, template, {'druzinka':druzinka, 'message':message})

            elif request.POST['x']==druzinka.me_x and request.POST['y']==druzinka.me_y:
                message = 'Posun na miesto kde práve stojíte nie je možný!'
                error = str(druzinka.nazov) + ' - ' + message
                Message.objects.create(text=error)
                return render(request, template, {'druzinka':druzinka, 'message':message})

            else:
                druzinka.me_x = request.POST['x']
                druzinka.me_y = request.POST['y']
                return HttpResponseRedirect(reverse('obdlznik:druzinka'))

        elif 'info' in request.POST:
            goal = Goal.objects.get(idDruzinka=druzinka, done=False)
            inf = choice(True, False)
            if inf:
                inf = (abs(goal.x - me_x) + 1)*(abs(goal.y - me_y) + 1)
            else:
                inf = 2*(abs(goal.x - me_x) + 1) + 2*(abs(goal.y - me_y) + 1)
            return render(request, template, {'druzinka':druzinka, 'information':inf})

        elif 'is_goal' in request.POST:
            goal = Goal.objects.get(idDruzinka=druzinka, done=False)
            if druzinka.me_x == goal.x and druzinka.me_y == goal.y:
                druzinka.goals += 1
                goal.end_time = timezone.now()
                goal.done = True
                Goal.objects.create(idDruzinka=druzinka, x=randint(0,20), y=randint(0,20))

                notification = str(druzinka.nazov) + ' - zistili polohu cieľa, bol vygenerovaný nový!'
                Message.objects.create(importance=True, text=notification)
                return HttpResponseRedirect(reverse('obdlznik:druzinka'))

            else:
                message = 'Nesprávny cieľ :('
                error = str(druzinka.nazov) + ' - ' + message
                Message.objects.create(text=error)
                return render(request, template, {'druzinka':druzinka, 'message':message})

    else:
        return render(request, template, {'druzinka':druzinka})

def opravovatel(request):
    template = 'obdlznik/opravovatel.html'
    druzinky = Druzinka.objects.all()

    if request.method == 'POST':
        try:
            druzinka = Druzinka.objects.get(pk=int(request.POST['druzinka']))
        except (TypeError, KeyError, ValueError, Druzinka.DoesNotExist):
            message = 'Vyber družinku!'
            error = 'Vedúcko opravovateľ - ' + message
            Message.objects.create(text=error)
            return render(request, template, {'druzinky':druzinky, 'message': message})

        try:
            druzinka.points += int(request.POST['points'])
        except (TypeError, KeyError, ValueError):
            message = 'Zadaj body!'
            error = 'Vedúcko opravovateľ - ' + message
            Message.objects.create(text=error)
            return render(request, template, {'druzinky':druzinky, 'message': message})

        druzinka.save()

        return redirect('/obdlznik/ulohy/')

    else:
        return render(request, template, {'druzinky': druzinky})

def spravca(request):
    template = 'obdlznik/spravca.html'
    druzinky = Druzinka.objects.all()
    messages = reversed(Message.objects.all())
    return render(request, template, {'druzinky':druzinky, 'messages':messages})
