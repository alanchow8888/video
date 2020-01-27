from django.conf.urls import include,url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from video import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^myadmin/', include('apps.myadmin.urls',namespace='myadmin')),
    url(r'^video/', include('apps.video.urls',namespace='video')),
    url(r'^face/', include('apps.face.urls',namespace='face')),
    url(r'^quiz/', include('apps.quiz.urls',namespace='quiz')),
    url(r'^user/', include('apps.user.urls',namespace='user')),
    url(r'^', views.Index.as_view(), name='login'),
]
urlpatterns += staticfiles_urlpatterns()
