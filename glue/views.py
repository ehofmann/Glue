from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login

from glue.models import Task

@login_required
def user_dashboard(request):
    todo_tasks = Task.objects.filter(finished=False)
    done_tasks = Task.objects.filter(finished=True)
    return render_to_response('glue/user_dashboard.html', {'todo_tasks': todo_tasks, 'done_tasks': done_tasks})

@login_required
def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render_to_response('glue/show_task.html', {'task': task})

@login_required
def select_task_project(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render_to_response('glue/show_task.html', {'task': task})

def logout_user(request):
    logout(request)
    return render_to_response('glue/logout.html', {'task': task})

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass
    