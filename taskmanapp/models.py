import datetime
from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import MinValueValidator

class Task(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE,blank=True,null=True,related_name='tasks')
    task_name = models.CharField(max_length=200)
    deadline = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    is_completed = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

class UserActivity(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity
