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
  actionsRequiringParameter = {}
  for task_action in task_actions:
    action = get_class(task_action.action.classname)(task_action)
    for param in action.get_required_parameters():
      if not param in actionsRequiringParameter:
        actionsRequiringParameter[param] = []
      actionsRequiringParameter[param].append(task_action.id);

  return render('glue/show_task.html', {'model': t, 'model_class': 'Task', 'model_actions': task_actions, 'actionsRequiringParameter': actionsRequiringParameter}, request)

@login_required
def task(request, task_id):
  return show_model(request, task_id, 'Task')

@login_required
def show_model(request, instance_id, model_class_name):
  init_actions()
  instance = get_object_or_404(get_class('glue.models.' + model_class_name), pk=instance_id)
  # the following could improve performance, but did not work once... maybe some kind
  # of cache issue. The taskactions where  not found.
  #task_actions = TaskAction.objects.select_related().filter(task=t)
  filt = {model_class_name.lower() : instance}
  model_actions = get_class('glue.action.' + model_class_name + 'Action').objects.filter(**filt)
  #print "task id %s: task_actions = %s" % (task_id, task_actions)
  actionsRequiringParameter = {}
  for model_action in model_actions:
    action = get_class(model_action.action.classname)(model_action)
    for param in action.get_required_parameters():
      if not param in actionsRequiringParameter:
        actionsRequiringParameter[param] = []
      actionsRequiringParameter[param].append(model_action.id);

  return render('glue/show_' + model_class_name.lower() + '.html', {'model': instance, 'model_class': model_class_name, 'model_actions': model_actions, 'actionsRequiringParameter': actionsRequiringParameter}, request)

@login_required
def create_component(request):
  return create(request, Component, ComponentForm, 'Component')

@login_required
def create_task(request):
  """
  Create or edit a task model instance.
  """
  def create_actions(task):
    """
    Creates a TaskAction instance for all actions and relates it to the task.
    """
    init_actions()
    for action in Action.objects.all():
      print "Creating TaskAction for task %s and action %s" % (task,action)
      new_taskaction = TaskAction(action=action, task=task)
      new_taskaction.save()
  return create(request, Task, TaskForm, 'Task', create_actions)

@login_required
def create(request, model_class, form_class, modelType, post_save_method=None):
  """
  Create or edit a model instance
  When the method is GET, then a form is shown, to either create or edit (if id is passed) the instance.
  When the method is POST, then we receive the results of the form and either update the model instance (if id is set) or create a new model instance.
  The GET or POST parameter "next" can be set to a template, that should be rendered.
  request -- The http request
  model_class -- The class (like model.Task)
  form_class -- The class of the form (like TaskForm)
  modelType -- The name of the model (like 'Task')
  post_save_method -- A method called after the model instance is saved, taking the model
                      instance as parameter.
  """
  if request.method == 'GET':
    # Show form
    id = request.GET.get('id')
    if id:
      next_link = request.GET.get('next')
      model = model_class.objects.get(id=id)
      form = form_class(instance=model) # An unbound form
      form.id = id
      form.next = next_link
      form.modelType = modelType
    else:
      print "create component create new"
      model = model_class()
      model.user = request.user
      form = form_class(instance=model) # An unbound form
      form.user = request.user
      form.modelType = modelType
    return render('glue/create_model.html', {'form': form}, request)

  elif request.method == 'POST': # If the form has been submitted...
    # evaluate form data and create or edit model instance

    # if there is an id parameter then get the corresponding model instance
    # otherwise create a new model instance
    id = request.POST.get('id')
    if id == '':
      model = model_class();
    else:
      model  = model_class.objects.get(id=id)
    
    # check that the POST data is valid and save the model instance
    form = form_class(request.POST, instance=model) # A form bound to the POST data
    form.modelType = modelType
    if form.is_valid(): # All validation rules pass
      model = form.save()
      
      # if available then execute the passed method
      if post_save_method != None:
        post_save_method(model)

      # Get the next page/link, from the POST, or redirect to dashboard
      next_link = request.POST.get('next')
      if next_link == '':
        next_link = "/glue/dashboard/"
      return HttpResponseRedirect(next_link) # Redirect after POST
    else:
      print "The form is not valid"
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
def get_component(request):
  """
  """
  response_dict = {}
  try:
    model_id = request.GET.get('project_id')
    model = get_object_or_404(Project, pk=model_id)
    data = serializers.serialize("json", [model])
    project = serializers.serialize("json", [model.project])

    response_dict.update({'component': component, 'project': project, 'component_id': task.component.id, 'project_id': task.component.project.id})
  except Exception as e:
    print e
    print "Unexpected error:", sys.exc_info()[0]
    return HttpResponse(str(e))
  response_dict.update({'success': True})
  return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');

@login_required
def get_task(request):
  """
  """
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

