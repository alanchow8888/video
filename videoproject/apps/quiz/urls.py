from django.urls import path
from . import views
from apps.quiz.views import *
app_name = 'quiz'
urlpatterns = [
    path('testrecord', testrecord, name='testrecord'),
]
