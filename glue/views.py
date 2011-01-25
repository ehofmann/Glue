from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from glue.models import *


# Create the form class.
class TaskForm(ModelForm):
    class Meta:
        model = Task

# Create the form class.
class ComponentForm(ModelForm):
    class Meta:
        model = Component

class ProjectForm(ModelForm):
    class Meta:
        model = Project

def render(template, context, request):
    return render_to_response(template, 
                              context,
                              context_instance=RequestContext(request))

@login_required
def user_dashboard(request):
    todo_tasks = Task.objects.filter(finished=False)
    done_tasks = Task.objects.filter(finished=True)
    return render('glue/user_dashboard.html', 
                              {'todo_tasks': todo_tasks, 'done_tasks': done_tasks},
                              request)

@login_required
def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render('glue/show_task.html', {'task': task}, request)


@login_required
def show_task_actions(request, task_id):
    t = get_object_or_404(Task, pk=task_id)
    task_actions = TaskAction.objects.select_related().filter(task=t)
    return render('glue/show_task_actions.html', {'task_actions': task_actions}, request)

@login_required
def show_task_action_table(request, task_id):
    t = get_object_or_404(Task, pk=task_id)
    TaskActionFormSet = modelformset_factory(TaskAction)
    formset = TaskActionFormSet(queryset=TaskAction.objects.select_related().filter(task=t))
    
    return render('glue/show_task_action_table.html', {'formset': formset}, request)


@login_required
def create_task(request):
    if request.method == 'POST': # If the form has been submitted...
        form = TaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/glue/dashboard/') # Redirect after POST
    else:
        form = TaskForm() # An unbound form
    return render('glue/create_task.html', {'form': form}, request)

@login_required
def create_component(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ComponentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/glue/dashboard/') # Redirect after POST
    else:
        form = ComponentForm() # An unbound form
    return render('glue/create_component.html', {'form': form}, request)

@login_required
def create_project(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ProjectForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/glue/dashboard/') # Redirect after POST
    else:
        form = ProjectForm() # An unbound form

    return render('glue/create_project.html', {'form': form}, request)
