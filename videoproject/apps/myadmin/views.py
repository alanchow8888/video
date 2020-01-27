from django.shortcuts import render
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import *
from django.http import JsonResponse
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic import View
from video.models import Video_user
import json

class list(View):
    def get(self, request):
        detail1 = Video_user.objects.filter(user=request.user,video=1).values()
        detail2 = Video_user.objects.filter(user=request.user,video=2).values()
        user = request.user
        content={'detail1':detail1,'detail2':detail2,'user':user}
        response = render(request, 'myadmin/list.html',{'content':content})
        return response

class Index(View):
    def get(self, request):
        content={}
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        content['username'] = username
        return render_to_response("myadmin/login.html",{'content': content})


def delete(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return JsonResponse({"code": 1, "msg": "无删除权限"})
        data = json.loads(request.body)
        video_id = data['video_id']
        times = data['times']
        videotime = data['videotime']
        instance = Video_user.objects.filter(user=request.user,video_id=video_id,video_time=videotime,times=times)
        instance.delete()
        return JsonResponse({"code": 0, "msg": "success"})


def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')
        remember = request.POST.get('remember')
        if(username=='' or password == ''):
            return render(request, 'myadmin/login.html', {'error': 0})
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                response =  redirect('/myadmin/list')
                if remember:
                    response.set_cookie('username',username,max_age=7*24*3600)
                auth_login(request, user)
                return response
            else:
                #return HttpResponseRedirect('/base/index.html/?error=error')
                return render(request, 'myadmin/login.html', {'error': 1})
    else:
        return redirect('/')
