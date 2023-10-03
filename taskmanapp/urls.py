from django.urls import path
from . import views
from .api import TaskListAPI, TaskDetailAPI


# User login System
urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]


# api
urlpatterns += [
    path('tasks/', TaskListAPI.as_view()),
    path('tasks/<id>', TaskDetailAPI.as_view()),

]

# Ajax
urlpatterns += [
    path('', views.profile, name='profile'),
    path('task-sort/', views.task_sort, name='task_sort'),
    path('task-save/', views.task_save, name='task_save'),
    path('task-delete/', views.task_delete, name='task_delete'),
    path('task-complete/', views.task_complete, name='task_complete'),
    path('task-incomplete/', views.task_incomplete, name='task_incomplete'),
    path('activity/', views.activity, name='activity'),

]


