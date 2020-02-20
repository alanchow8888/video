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
import os

class list(View):
    def get(self, request):
        if not request.user.is_superuser:
            return render(request, 'myadmin/login.html', {'error': 4})
        else:
            content={}
            picture_path=os.getcwd()+"/static/data/picture/"
            fileList = os.listdir(picture_path)
            fileList.remove('1.txt');
            fileList.remove('root');
            content['filelist']= fileList
            #detail1 = Video_user.objects.filter(user=request.user,video=1).values()
            #detail2 = Video_user.objects.filter(user=request.user,video=2).values()
            #user = request.user
            #content={'detail1':detail1,'detail2':detail2,'user':user}
            content2={}
            content2['val']={'filelist':['a','b'],'size':['1','2']}
            print(content2)
            response = render(request, 'myadmin/list.html',{'content':content2})
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

class query_result(View):
    def get(self, request,user,times,**kwargs):
        if not request.user.is_superuser:
            return render(request, 'myadmin/login.html', {'error': 4})
        else:
            content={}
            internal="/static/data/picture/"+user+"/video1/"+str(times)+"/"
            picture_path=os.getcwd()+internal
            fileList = os.listdir(picture_path)
            n=[ internal+x for x in fileList ]
            content=n
            return render_to_response("myadmin/list2.html",{'content': content})


def query_path(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return JsonResponse({"code": 0, "msg": "无权限"})
        else:
            data = json.loads(request.body)
            user_name = data['user']
            picture_path=os.getcwd()+"/static/data/picture/"
            personfile = os.listdir(picture_path+user_name+'/video1/')
            str = '["'+'","'.join(personfile)+'"]'
            content = '{"data":'+str+'}'
            return HttpResponse(content)


def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')

        if(username=='' or password == ''):
            return render(request, 'myadmin/login.html', {'error': 0})
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                response =  redirect('/myadmin/list')
                auth_login(request, user)
                return response
            else:
                #return HttpResponseRedirect('/base/index.html/?error=error')
                return render(request, 'myadmin/login.html', {'error': 1})
    else:
        return redirect('/')
