from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class SignUpForm(UserCreationForm):
 password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput)
 class Meta:
  model = User
  fields = ['username', 'email']
  labels = {'email': 'Email'}


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'deadline']
        widgets = {
            'deadline': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}
            )
        }
