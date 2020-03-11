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
import re
import time

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
            #content['val']={'filelist':['a','b'],'size':['1','2']}
            #content['val2']={'filelist':['c','d'],'size':['2','3']}

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

class query_result(View):
    def get(self, request,user,times,**kwargs):
        if not request.user.is_superuser:
            return render(request, 'myadmin/login.html', {'error': 4})
        else:
            content={}
            answer_list=[]
            internal="/static/data/picture/"+user+"/video1/"+str(times)+"/"
            picture_path=os.getcwd()+internal
            fileList = os.listdir(picture_path)
            n=[ internal+x for x in fileList ]
            content=n
            try:
                with open(os.getcwd()+"/static/data/answer/"+user+"/video1/"+str(times)+"/answer.txt", "r") as f:
                    for line in f.readlines():
                        line = line.strip('\n')  #去掉列表中每一个元素的换行符
                        number = re.findall("Question:(.*),",line)
                        if(number[0]=='1'):
                            if(line[-1]=='4'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='2'):
                            if(line[-1]=='1'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='3'):
                            if(line[-1]=='1'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='4'):
                            if(line[-1]=='3'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='5'):
                            if(line[-1]=='3'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='6'):
                            if(line[-1]=='a'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='7'):
                            if(line[-1]=='1'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='8'):
                            if(line[-1]=='3'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='9'):
                            if(line[-1]=='4'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        elif(number[0]=='10'):
                            if(line[-1]=='2'):
                                line = line +' (Right)'
                            else:
                                line = line +' (Error)'
                        answer_list.append(line)
            except:
                answer_list=['no answer record']

            return render_to_response("myadmin/list2.html",{'content': content,'answer':answer_list})

def getdirsize(dir):
   size = 0
   for root, dirs, files in os.walk(dir):
      size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
   return size

def query_path(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return JsonResponse({"code": 0, "msg": "无权限"})
        else:
            size=[]
            size2=[]
            create_time=[]
            last_time=[]
            data = json.loads(request.body)
            user_name = data['user']
            picture_path=os.getcwd()+"/static/data/picture/"
            personfile = os.listdir(picture_path+user_name+'/video1/')
            personfile1 = [int(x) for x in personfile]
            personfile=[str(x) for x in sorted(personfile1)]

            for i in personfile:
                size.append(len(os.listdir(picture_path+user_name+'/video1/'+i+'/')))
                size2.append(getdirsize(picture_path+user_name+'/video1/'+i+'/'))
                create_time.append(time.ctime(os.path.getctime(picture_path+user_name+'/video1/'+i+'/')))
                last_time.append(time.ctime(os.path.getmtime(picture_path+user_name+'/video1/'+i+'/')))

            str1 = '["'+'","'.join(personfile)+'"]'
            str2 = '["'+'","'.join('%s' %id for id in size)+'"]'
            size2=[x/(1024*1024) for x in size2]
            str2 = '["'+'","'.join('%s' %id for id in size)+'"]'
            size2= '["'+'","'.join('%0.4s' %id for id in size2)+'"]'
            create_time_list = '["'+'","'.join('%s' %id for id in create_time)+'"]'
            last_time_list  = '["'+'","'.join('%s' %id for id in last_time)+'"]'
            content = '{"data":'+str1+','+'"size":'+str2+','+'"size2":'+size2+','+'"create_time":'+create_time_list+','+'"last_time":'+last_time_list+'}'
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
