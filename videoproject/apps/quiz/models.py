from django.db import models
from django.conf import settings
# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    class Meta:
        db_table = "v_class"

class Question(models.Model):
    LEVEL_CHOICES = (
            ('0', 'low'),
            ('1', 'high'),
    )
    name = models.CharField(max_length=100,blank=True, null=True)
    level = models.CharField(max_length=1 ,choices=LEVEL_CHOICES,blank=True, null=True)
    class_id = models.ForeignKey(Class,on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = "v_question"

class Choice(models.Model):
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE, null=True)
    question_content = models.CharField(max_length=255,blank=True, null=True)
    option_1 = models.CharField(max_length=255,blank=True, null=True)
    option_2 = models.CharField(max_length=255,blank=True, null=True)
    option_3 = models.CharField(max_length=255,blank=True, null=True)
    option_4 = models.CharField(max_length=255,blank=True, null=True)
    answer = models.CharField(max_length=255,blank=True, null=True)
    video_time = models.CharField(max_length=255,blank=True, null=True)
    class Meta:
        db_table = "v_choice"

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=255,blank=True, null=True)
    class Meta:
        db_table = "v_answer"
