# Generated by Django 2.2.5 on 2019-11-08 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191108_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150),
        ),
    ]
