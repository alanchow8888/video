from django.shortcuts import *
from django.views.generic import View
from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.decorators.http import require_http_methods
from video.models import Video,Video_user
from django.db.models import Max
from quiz.models import Choice
import json
import base64
import os
import re


class Index(View):
    def get(self, request):
        content={}
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        content['username'] = username
        return render_to_response("base/index.html",{'content': content})


class videolist(View):
    def get(self, request,video_id):
        content={}
        if request.user.is_authenticated:
            content['video_list'] = Video.objects.filter(id=video_id).values()[0]
            content['video_id'] = video_id
            if(Video_user.objects.filter(user_id=request.user.id,video_id=video_id).exists()):
                video_times=Video_user.objects.filter(user_id=request.user.id,video_id=video_id).values("times")[0]['times']+int(1)
                #Video_user.objects.filter(user_id=request.user.id,video_id=video_id).update(times=new_time)
            else:
                video_times=0
                #Video_user.objects.create(user_id=request.user.id,times=1,video_id=video_id)
            response = render(request, 'base/video.html',{'content':content})
            response.set_signed_cookie('video_id', video_id)
            response.set_signed_cookie('video_times', video_times)
            return response

        else:
            return redirect('/')

def record(request):
    if request.method == 'POST':
        postBody = request.body
        video_id = json.loads(postBody)['video_id']
        video_times =  json.loads(postBody)['video_times']
        imgdata=json.loads(postBody)['uploadImg']
        timeline=json.loads(postBody)['videotime']
        imgdata64 = base64.b64decode(imgdata)
        #if(timeline == 0):
        Video_user.objects.create(user_id=request.user.id,times=video_times,video_id=video_id,picture=imgdata,video_time=timeline)
        imgpath='static//data//picture//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//'+str(timeline)+'_'+'0'+'.jpg'
        if(os.path.exists(imgpath)):
            li=[]
            for filename in os.listdir('static//data//picture//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//'):
                 li.append(re.findall( str(timeline)+'_(.*).jpg', filename))
            imgpath='static//data//picture//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//'+str(timeline)+'_'+str(int(max(li)[0])+1)+'.jpg'
        file = open(imgpath,'wb')
        file.write(imgdata64)
        file.close()
        res_json = '{"data":"'+str(timeline)+'"}'
        print(res_json)
        return HttpResponse(res_json)


class partlist(View):
    def get(self, request,page_id,**kwargs):
        content = {}
        if request.user.is_authenticated:

            if(page_id == 2):
                video_id = request.GET.get('video_id','1')
                if(Video_user.objects.filter(user_id=request.user.id,video_id=video_id).exists()):
                    video_times=Video_user.objects.filter(user_id=request.user.id,video_id=video_id).aggregate(Max('times'))['times__max']+int(1)#.values("times")[0]['times']+int(1)
                    print(video_times)
                else:
                    video_times = 1

                mkdir = ('static//data//picture//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//')
                isExists = os.path.exists(mkdir)
                if not isExists:
                    os.makedirs(mkdir)
                mkdir2 = ('static//data//answer//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//')
                isExists2 = os.path.exists(mkdir2)
                if not isExists2:
                    os.makedirs(mkdir2)

                video_obj = Video.objects.filter(id=video_id).values()[0]
                content = {'video_id':video_id,'video_times':video_times,'video_obj':video_obj}

            response = render(request, 'part/part'+str(page_id)+'.html',content)
            return response
        else:
            return redirect('/')
