# Generated by Django 2.2.5 on 2019-11-08 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191108_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30),
        ),
    ]
