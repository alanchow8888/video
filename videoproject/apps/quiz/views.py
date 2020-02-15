from django.shortcuts import *
from django.views.generic import View
from django.shortcuts import render,render_to_response
import json
from django.http import JsonResponse
from quiz.models import Answer,Question
# Create your views here.
def testrecord(request):
    if request.method == 'POST':
        postBody = request.body
        answer = json.loads(postBody)['answer']
        question_id = json.loads(postBody)['question_id']
        video_times = json.loads(postBody)['video_times']
        video_id = 1
        with open('static//data//answer//'+str(request.user)+'//video'+str(video_id)+'//'+str(video_times)+'//answer.txt','a') as file:
            file.write("Question:"+str(question_id)+','+"Answer:"+str(answer)+"\n")

        #aid = Question.objects.get(id=int(question_id))
        #Answer.objects.create(user_id=request.user.id,question_id=aid,answer=answer)
        return JsonResponse({"code": 0, "msg": "success"})
