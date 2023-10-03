from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, HttpResponse
from .forms import SignUpForm, TaskForm
from .models import Task, UserActivity
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse


# Signup View Function
def sign_up(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = SignUpForm(request.POST)
            if fm.is_valid():
                messages.success(request, 'Account Created Successfully !!')
                fm.save()
                return redirect('profile')

        else:
            fm = SignUpForm()
        return render(request, 'taskmanapp/signup.jinja', {'form': fm})
    else:
        return redirect('profile')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url='login')
def activity(request):
    activity_list = UserActivity.objects.filter(
        user=request.user).order_by('-added_on')
    context = {'activity_list': activity_list}
    return render(request, 'taskmanapp/activity.jinja', context)


# Login View Function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            try:
                user_by_email = User.objects.filter(email=email).first()
                if user_by_email:
                    username = user_by_email.username
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Logged in successfully !!')
                        return redirect('profile')
                    else:
                        messages.error(
                            request, 'Email or password does not correct')
                        return render(request, 'taskmanapp/login_email.jinja')
                else:
                    messages.error(
                        request, 'Email or password does not correct')
                    return render(request, 'taskmanapp/login_email.jinja')

            except:
                messages.error(request, 'Email or password does not correct')
                return render(request, 'taskmanapp/login_email.jinja')

        else:
            return render(request, 'taskmanapp/login_email.jinja')
    else:
        return redirect('profile')

    # Task Create View Ajax


@login_required(login_url='login')
def profile(request):
    if request.user.is_authenticated:
        form = TaskForm()
        return render(request, 'taskmanapp/profile.jinja', {'form': form,'name': request.user})
    else:
        return HttpResponseRedirect('/login/')



# Task Save Ajax
@login_required(login_url='login')
def task_save(request):
    if request.method == "POST":
        task_name = request.POST['id_task_name']
        deadline = request.POST['id_deadline']
        user = request.user
        task =  Task.objects.create(task_name=task_name,deadline=deadline,user=user)
        try:
            task.save()
            return redirect('task_sort')

        except:
            return JsonResponse({'status': '0'})
        

@login_required(login_url='login')
def task_delete(request):
    task_id = request.POST['id_task_id']
    user = request.user
    task = get_object_or_404(Task, id=task_id)
    try:
        task.delete()
        return redirect('task_sort')
    except:
        return JsonResponse({'status': '0'})
    

@login_required(login_url='login')
def task_complete(request):
    task_id = request.POST['id_task_id']
    user = request.user
    task = get_object_or_404(Task, id=task_id)
    try:
        task.is_completed = True
        task.save()
        return redirect('task_sort')
    except:
        return JsonResponse({'status': '0'})


@login_required(login_url='login')
def task_incomplete(request):
    task_id = request.POST['id_task_id']
    user = request.user
    task = get_object_or_404(Task, id=task_id)
    try:
        if task.user == request.user:
            task.is_completed = False
            task.save()
            return redirect('task_sort')
    except:
        return JsonResponse({'status': '0'})
    

@login_required(login_url='login')
def task_sort(request):
    try:
 
        order = request.POST.get('order')
        sort_by = request.POST.get('sort_by')
        print(order)
        print(sort_by)

        if order is not None:
            request.session['order'] = order
            request.session['sort_by'] = sort_by
        else:
            order = request.session.get('order')
            sort_by = request.session.get('sort_by')


        print(order)
        print(sort_by)
        if sort_by not in ['task_name', 'deadline', 'added_on','is_completed']:
            sort_by = 'task_name'

        if order not in ['asc', 'desc']:
            order = 'asc'

        user_task_list = Task.objects.filter(user=request.user)

        if order == 'asc':
            user_task_list = user_task_list.order_by(sort_by).values()
        else:
            user_task_list = user_task_list.order_by(f'-{sort_by}').values()
        return JsonResponse({'status': 'Save' ,'user_task_list':list(user_task_list)})
    except Exception as e:
        print(e)
        return JsonResponse({'status': '0'})