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
                              {'todo_tasks': todo_tasks, 'done_tasks': done_tasks},
                              request)

@login_required
def task(request, task_id):
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
    if request.method == 'POST': # If the form has been submitted...
        form = TaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            task = form.save()
	    #Create taskactions for task
	    init_actions()
	    for action in Action.objects.all():
		new_taskaction = TaskAction(action=action, task=task)
		new_taskaction.save()

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

    	response_dict.update({'task': data, 'component': component, 'project': project})
	
    except Exception as e:
	print e
	print "Unexpected error:", sys.exc_info()[0]
    	return HttpResponse(str(e))
    response_dict.update({'success': True})
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');

#@login_required
#def show_task_actions(request, task_id):
#    t = get_object_or_404(Task, pk=task_id)
#    task_actions = TaskAction.objects.select_related().filter(task=t)
#    return render('glue/show_task_actions.html', {'task_actions': task_actions}, request)


#@login_required
#def show_task_action_table(request, task_id):
#    t = get_object_or_404(Task, pk=task_id)
#    task_actions = TaskAction.objects.select_related().filter(task=t, before_development=True)
#    #TaskActionFormSet = inlineformset_factory(TaskAction, Task, extra=0)
#    #formset = TaskActionFormSet(queryset=TaskAction.objects.select_related().filter(task=t))
#
#    return render('glue/show_task_action_table.html', {'task_actions': task_actions}, request)
#
#
#@login_required
#def show_actions_before(request, task_id):
#    t = get_object_or_404(Task, pk=task_id)
#    task_actions = TaskAction.objects.select_related().filter(task=t, before_development=False)
#    #TaskActionFormSet = inlineformset_factory(TaskAction, Task, extra=0)
#    #formset = TaskActionFormSet(queryset=TaskAction.objects.select_related().filter(task=t))
#
#    return render('glue/show_task_action_table.html', 
#                  {'task_actions': task_actions, 
#                   'next_step': '/glue/do_actions/%s/before' % task_id},
#                    request)
#

#@login_required
#def show_actions_after(request, task_id):
#    t = get_object_or_404(Task, pk=task_id)
#    task_actions = TaskAction.objects.select_related().filter(task=t, before_development=false)
#    #TaskActionFormSet = inlineformset_factory(TaskAction, Task, extra=0)
#    #formset = TaskActionFormSet(queryset=TaskAction.objects.select_related().filter(task=t))
#
#    return render('glue/show_task_action_table.html', 
#                  {'task_actions': task_actions, 
#                   'next_step': '/glue/do_actions/%s/after' % task_id},
#                    request)
#

#@login_required
#def do_actions(request, task_id, when):
#    is_before = when == 'before'
#    t = get_object_or_404(Task, pk=task_id)
#    task_actions = TaskAction.objects.select_related().filter(task=t, 
#	before_development=is_before,
#	enabled=True,
#	visible=True)
#
#    manager = ActionManager(task_actions)
#    action_results = manager.execute()
#
#    return render('glue/action_results.html', {'action_results': action_results}, request)
