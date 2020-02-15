from django.conf.urls import include,url
from django.urls import path
from apps.video.views import *
from apps.user.views import *
app_name = 'video'

urlpatterns = [
    path('index', Index.as_view(), name='index'),
    #path('test', IndexView.as_view(), name='IndexView'),
    path('record', record, name='record'),
    path('part<int:page_id>', partlist.as_view(), name='partlist'),
    path('calibration', calibration, name='calibration'),
]
