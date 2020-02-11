from django.db import models
from django.conf import settings
# Create your models here.
from quiz.models import Class

class Video(models.Model):
    LEVEL_CHOICES = (
            ('0', 'low'),
            ('1', 'high'),
    )
    title = models.CharField(max_length=255,blank=True, null=True)
    desc = models.CharField(max_length=255,blank=True, null=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=10000,blank=True, null=True)
    view_count = models.IntegerField(default=0, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, max_length=20)
    level = models.CharField(max_length=1 ,choices=LEVEL_CHOICES,blank=True, null=True)
    class Meta:
        db_table = "v_video"
        verbose_name = "video information"


class Video_user(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    times = models.IntegerField(default=0 ,blank=True)
    video_time = models.CharField(max_length=255,blank=True, null=True)
    picture = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "v_video_user"
        verbose_name = "user_record"
