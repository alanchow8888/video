# Generated by Django 2.2.5 on 2019-11-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20191125_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video_user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='photos'),
        ),
    ]
