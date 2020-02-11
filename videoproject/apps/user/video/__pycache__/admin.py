from django.contrib import admin

from video.models import Video,Classification,Video_user
admin.site.register(Video)
admin.site.register(Classification)
admin.site.register(Video_user)
