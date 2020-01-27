from django.urls import path
from apps.myadmin.views import *
app_name = 'myadmin'
urlpatterns = [
    path('login/', login, name='login'),
    path('delete/', delete, name='delete'),
    path('', Index.as_view(), name='index'),
    path('list', list.as_view(),  name='list'),
]
