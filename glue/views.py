from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers

from glue.models import *
from glue.action import ActionManager, init_actions, get_class
from django import forms
import sys

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
                              #{'todo_tasks': todo_tasks, 'done_tasks': done_tasks},
                              {'task_groups': {'Done': done_tasks, 'Todo': todo_tasks}},
                              request)

@login_required
def task(request, task_id):
    init_actions()
    t = get_object_or_404(Task, pk=task_id)
    # the following could improve performance, but did not work once... maybe some kind
    # of cache issue. The taskactions where  not found.
    #task_actions = TaskAction.objects.select_related().filter(task=t)
    task_actions = TaskAction.objects.filter(task=t)
    print "task id %s: task_actions = %s" % (task_id, task_actions)
    #parameter_dependencies = {}
    actionsRequiringParameter = {}
    for task_action in task_actions:
	action = get_class(task_action.action.classname)(task_action)
	#parameter_dependencies[task_action.id] = (action.get_required_parameters(), action.get_provided_parameters())
	for param in action.get_required_parameters():
		if not param in actionsRequiringParameter:
			actionsRequiringParameter[param] = []
		actionsRequiringParameter[param].append(task_action.id);

    return render('glue/show_task.html', {'task': t, 'task_actions': task_actions, 'actionsRequiringParameter': actionsRequiringParameter}, request)

@login_required
def create_task(request):
    print "create task"
    if request.method == 'GET': # If the form has been submitted...
        print "method %s" % request.method
        print "trying to get the task id"
        id = request.GET.get('id')
        task = Task.objects.get(id=id)
        form = TaskForm(instance=task) # An unbound form
    elif request.method == 'POST':
	form = TaskForm(request.POST) # A form bound to the POST data
	if form.is_valid(): # All validation rules pass
	    task = form.save()
	    #Create taskactions for task
	    init_actions()
	    for action in Action.objects.all():
		print "Creating TaskAction for task %s and action %s" % (task,action)
		new_taskaction = TaskAction(action=action, task=task)
		new_taskaction.save()
	    return HttpResponseRedirect('/glue/dashboard/') # Redirect after POST
    else:
        form = TaskForm() # An unbound form
    return render('glue/create_task.html', {'form': form}, request)

@login_required
def create_component(request):
	return create(request, Component, ComponentForm, 'Component')

@login_required
def create(request, model_class, form_class, modelType):
    if request.method == 'GET': # If the form has been submitted...
	id = request.GET.get('id')
	next_link = request.GET.get('next')
	model = model_class.objects.get(id=id)
	form = form_class(instance=model) # An unbound form
	form.id = id
	form.next = next_link
	form.modelType = modelType
    elif request.method == 'POST': # If the form has been submitted...
	id = request.POST.get('id')
	next_link = request.GET.get('next')
	model  = model_class.objects.get(id=id)
	form = form_class(request.POST, instance=model) # A form bound to the POST data
	if form.is_valid(): # All validation rules pass
	    model = form.save()
	    return HttpResponseRedirect(next_link) # Redirect after POST
		
    else:
	print "create component create new"
        form = ComponentForm() # An unbound form
    return render('glue/create_model.html', {'form': form}, request)

@login_required
def create_project(request):
	return create(request, Project, ProjectForm, 'Project')

@login_required
def do_action(request):
    print "do_action"
    response_dict = {}
    try:
	    task_action_id = request.GET.get('task_action_id')
	    print "Searching action"
	    task_action = get_object_or_404(TaskAction, pk=task_action_id)
	    print "Creating manager"
	    manager = ActionManager([task_action])
	    print "Executing manager"
	    action_results = manager.execute()
	    print "Printing results"
	    print str(action_results)
    except Exception as e:
	print e
	print "Unexpected error:", sys.exc_info()[0]
    	return HttpResponse(str(e))
    response_dict.update({'success': True})
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');


@login_required
def update_task_action(request):
    response_dict = {}
    try:
	task_action_id = request.GET.get('task_action_id')
	enabled = request.GET.get('enabled') == "true"
	finished = request.GET.get('finished') == "true"
	print "%s,%s,%s" % (task_action_id, enabled, finished)

	task_action = get_object_or_404(TaskAction, pk=task_action_id)
	task_action.enabled = enabled
	task_action.finished = finished
	task_action.save()
	
    except Exception as e:
	print e
	print "Unexpected error:", sys.exc_info()[0]
    	return HttpResponse(str(e))
    response_dict.update({'success': True})
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');


@login_required
def get_task(request):
    response_dict = {}
    try:
	task_id = request.GET.get('task_id')
	task = get_object_or_404(Task, pk=task_id)
	data = serializers.serialize("json", [task])
	component = serializers.serialize("json", [task.component])
	project = serializers.serialize("json", [task.component.project])

    	response_dict.update({'task': data, 'component': component, 'project': project, "task_id": task.id, 'component_id': task.component.id, 'project_id': task.component.project.id})
	
    except Exception as e:
	print e
	print "Unexpected error:", sys.exc_info()[0]
    	return HttpResponse(str(e))
    response_dict.update({'success': True})
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');

