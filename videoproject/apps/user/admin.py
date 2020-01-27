from django.contrib import admin

# Register your models here.

# Register your models here.
from user.models import User
#admin.site.register(User)
from django.contrib.auth.admin import UserAdmin
admin.site.register(User, UserAdmin)
