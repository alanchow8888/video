from django.urls import path
from apps.myadmin.views import *
app_name = 'myadmin'
urlpatterns = [
    path('login/', login, name='login'),
    path('query_path/', query_path, name='query_path'),
    path('query_result/<user>/<int:times>/', query_result.as_view(), name='query_result'),
    path('', Index.as_view(), name='index'),
    path('list', list.as_view(),  name='list'),
]
