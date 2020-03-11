from django.shortcuts import *
from django.views.generic import View
from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.decorators.http import require_http_methods
from video.models import Video,Video_user
from django.http import HttpResponseRedirect
from django.db.models import Max
from quiz.models import Choice
import json
import base64
import os
import re
import base64
from io import BytesIO
import cv2
import numpy as np
import re
import os
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import mimetypes
CASC_PATH = './apps/face/haarcascade_frontalface_default.xml'
cascade_classifier = cv2.CascadeClassifier(CASC_PATH)
class Index(View):
    def get(self, request):
        content={}
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        if 'rememberpsw' in request.COOKIES:
            rememberpsw = request.COOKIES['rememberpsw']
        else:
            rememberpsw = ''
        content['username'] = username
        content['rememberpsw'] = rememberpsw
        return render_to_response("base/index.html",{'content': content})



def calibration(request):
    if request.method == 'POST':
        postBody = request.body
        img = json.loads(postBody)['uploadImg']
        byte_data = base64.b64decode(img)
        img_array = np.fromstring(byte_data, np.uint8)
        image = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
        faces = cascade_classifier.detectMultiScale(
        image,
        scaleFactor = 1.2,
        minNeighbors = 5
        )
        print(faces)
        if(faces==()):
            content = '{"data":"failure"}'
            return HttpResponse(content)
        else:
            content = '{"data":"pass"}'
            return HttpResponse(content)
        """
        #import face_recognition
        #image_data = BytesIO(byte_data)
        #face = face_recognition.load_image_file(image_data)
        #face_locations = face_recognition.face_locations(face)
        """


def record(request):
    if request.method == 'POST':
        postBody = request.body
        video_id = json.loads(postBody)['video_id']
        video_times =  json.loads(postBody)['video_times']
        imgdata=json.loads(postBody)['uploadImg']
        timeline=json.loads(postBody)['videotime']
        imgdata64 = base64.b64decode(imgdata)
        img=''
        timeline2=''
        #if(timeline == 0):#picture=image,video_time=timeline
        Video_user.objects.create(user_id=request.user.id,times=video_times,video_id=video_id,picture=img,video_time=timeline2)
        imgpath='static//data//picture//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//'+str(timeline)+'_'+'0'+'.jpg'
        if(os.path.exists(imgpath)):
            li=[]
            for filename in os.listdir('static//data//picture//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//'):
                 key=re.findall(str(timeline)+'_(.*).jpg', filename)
                 if(len(key)):
                     li.append(int(key[0]))
            imgpath='static//data//picture//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//'+str(timeline)+'_'+str(int(max(li))+1)+'.jpg'
        file = open(imgpath,'wb')
        file.write(imgdata64)
        file.close()
        res_json = '{"data":"'+str(timeline)+'"}'
        return HttpResponse(res_json)


class partlist(View):
    def get(self, request,page_id,**kwargs):
        content = {}
        if request.user.is_authenticated:
            if(page_id == 2):
                try:
                    #passfail = request.COOKIES['p2']
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
                    #video_obj = Video.objects.filter(id=video_id).values()[0]
                    content = {'video_id':video_id,'video_times':video_times}
                    response = render(request, 'part/part'+str(page_id)+'.html',content)
                    return response
                except Exception as e:
                    print(e)
                    response = render(request, 'part/part1.html',content)
                    return response
            if(page_id == 1 or page_id == 3 ):
                response = render(request, 'part/part'+str(page_id)+'.html',content)
                return response
        else:
            return redirect('/')

def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data

def stream_video(request):
    """ responds to the video file as """
    path='static/media/v2.mp4'
    print(path)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        if first_byte:
            first_byte = int(first_byte)
        else:
             first_byte = 0
        last_byte = first_byte + 1024 * 1024 * 8 # 8M per piece, the maximum volume of the response body
        print(first_byte)
        print(last_byte)
        print(size)
        if last_byte > size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
                 # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
