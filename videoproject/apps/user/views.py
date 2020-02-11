from django.shortcuts import render
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import *
from django.views import generic
from django.http import HttpResponseRedirect


def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')
        remember = request.POST.get('remember')
        rememberpsw = request.POST.get('rememberpsw')
        print(username,password)

        if(username==''):
            return render(request, 'base/index.html', {'error': 0})
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                response =  redirect('/video/part1')
                if remember:
                    response.set_cookie('username',username,max_age=1*24*3600)
                if rememberpsw:
                    response.set_cookie('rememberpsw',password,max_age=1*24*3600)
                auth_login(request, user)
                return response
            else:
                #return HttpResponseRedirect('/base/index.html/?error=error')
                return render(request, 'base/index.html', {'error': 1})
    else:
        return redirect('/')

def logout(request):
    auth_logout(request)
    return render(request, 'base/index.html')
