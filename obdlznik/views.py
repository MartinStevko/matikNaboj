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
    try:
        druzinka = Druzinka.objects.get(idUser=request.user)
    except(KeyError, ValueError, Druzinka.DoesNotExist):
        message = 'K používateľovi ' + request.user.username + ', pod ktorým si prihlásený/á, družinka neexistuje!'
        return render(request, 'obdlznik/none.html', {'message':message})

    template = 'obdlznik/druzinka.html'

    if request.method == 'POST':
        if 'move' in request.POST:
            try:
                x = int(request.POST['x'])
                y = int(request.POST['y'])
            except(ValueError, TypeError, KeyError):
                message = 'Zadajte súradnice cieleného políčka, alebo naň kliknite!'
                error = str(druzinka.name) + ' - ' + message
                Message.objects.create(text=error)
                return render(request, template, {'druzinka':druzinka, 'message':message})

            if x!=druzinka.me_x and y!=druzinka.me_y:
                message = 'Posun je možný iba po jednej osi, nie oboch!'
                error = str(druzinka.name) + ' - ' + message
                Message.objects.create(text=error)
                return render(request, template, {'druzinka':druzinka, 'message':message})

            elif x==druzinka.me_x and y==druzinka.me_y:
                message = 'Posun na miesto kde práve stojíte nie je možný!'
                error = str(druzinka.name) + ' - ' + message
                Message.objects.create(text=error)
                return render(request, template, {'druzinka':druzinka, 'message':message})

            else:
                druzinka.points -= 1
                druzinka.me_x = x
                druzinka.me_y = y
                druzinka.save()

                return redirect('/obdlznik/hra/')

        elif 'info' in request.POST:
            goal = Goal.objects.get(idDruzinka=druzinka, done=False)
            inf = choice([True, False])
            if inf:
                inf = 'Vaša informácia je ' + str((abs(goal.x - druzinka.me_x) + 1)*(abs(goal.y - druzinka.me_y) + 1))
            else:
                inf = 'Vaša informácia je ' + str(2*(abs(goal.x - druzinka.me_x) + 1) + 2*(abs(goal.y - druzinka.me_y) + 1))

            druzinka.points -= 1
            druzinka.save()

            return render(request, template, {'druzinka':druzinka, 'information':inf})

        elif 'is_goal' in request.POST:
            goal = Goal.objects.get(idDruzinka=druzinka, done=False)
            druzinka.points -= 1
            druzinka.save()

            if druzinka.me_x == goal.x and druzinka.me_y == goal.y:
                druzinka.goals += 1
                druzinka.save()

                goal.end_time = timezone.now()
                goal.done = True
                goal.save()

                Goal.objects.create(idDruzinka=druzinka, x=randint(0,20), y=randint(0,20))

                notification = str(druzinka.name) + ' - zistili polohu cieľa, bol vygenerovaný nový!'
                Message.objects.create(importance=True, text=notification)
                return redirect('/obdlznik/hra/')

            else:
                not_goal = 'Cieľ je nesprávny :('
                error = str(druzinka.name) + ' - ' + not_goal
                Message.objects.create(text=error)
                return render(request, template, {'druzinka':druzinka, 'not_goal':not_goal})

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
