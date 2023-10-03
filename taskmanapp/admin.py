from django.contrib import admin
from .models import Task,UserActivity
# Register your models here.

admin.site.register(Task)
admin.site.register(UserActivity)
