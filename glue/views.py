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
def show_model(request, instance_id, model):
  model_class_name = model.capitalize()
  init_actions()
  instance = get_object_or_404(get_class('glue.models.' + model_class_name), pk=instance_id)
  # the following could improve performance, but did not work once... maybe some kind
  # of cache issue. The taskactions where  not found.
  #task_actions = TaskAction.objects.select_related().filter(task=t)
  filt = {model_class_name.lower() : instance}
  model_actions = get_class('glue.models.' + model_class_name + 'Action').objects.filter(**filt)
  #print "task id %s: task_actions = %s" % (task_id, task_actions)
  actionsRequiringParameter = {}
  model_action_id_numbers_map = {}
  i = 0
  for model_action in model_actions:
    model_action_id_numbers_map[model_action.id] = i
    i += 1
  
  for model_action in model_actions:
    action = get_class(model_action.action.classname)(model_action)
    for param in action.get_required_parameters():
      if not param in actionsRequiringParameter:
        actionsRequiringParameter[param] = []
      actionsRequiringParameter[param].append(model_action.id);
  
  return render('glue/show_model.html', {'model': instance, 'model_class': model_class_name, 'model_actions': model_actions, 'actionsRequiringParameter': actionsRequiringParameter, 'model_action_id_numbers_map': model_action_id_numbers_map}, request)

@login_required
def create_model(request, modelType):
  """
  Creates or edits a model instance. Adds task actions if a task is created.
  request -- the http request
  modelType -- name of the model in lower case like 'task'
  """
  #post_save_method=None
  print "Model type: '%s'" % modelType
  #if modelType == 'task':
  def create_actions(model):
    """
    Creates a TaskAction instance for all actions and relates it to the task.
    """
    init_actions()
    nr = 0;
    for action in Action.objects.filter(model_name=modelType):
      print "Creating TaskAction for %s %s and action %s" % (modelType, model,action)
      nr += 1;
      filt = {'action': action, modelType : model, 'nr' : nr}
      model_action_class = get_class('glue.models.' + modelType.capitalize() + 'Action')
      new_taskaction = model_action_class(**filt)
      new_taskaction.save()
  print "Setting create_actions as post_save_method"
  post_save_method = create_actions
      
  return generic_create_model(request, modelType, post_save_method)

@login_required
def generic_create_model(request, modelType, post_save_method=None):
  """
  Create or edit a model instance
  When the method is GET, then a form is shown, to either create or edit (if id is passed) the instance.
  When the method is POST, then we receive the results of the form and either update the model instance (if id is set) or create a new model instance.
  The GET or POST parameter "next" can be set to a template, that should be rendered.
  request -- The http request
  modelType -- name of the model, lower case ('task')
  post_save_method -- A method called after the model instance is saved, taking the model
                      instance as parameter.
  """
  full_model_name = 'glue.models.' + modelType.capitalize()
  model_class = get_class(full_model_name)
  #form_class -- The class of the form (like TaskForm)
  form_class = get_class('glue.views.' + modelType.capitalize() + 'Form')
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
      form.modelType = modelType.capitalize()
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

#@login_required
#def do_action(request):
#  print "do_action"
#  response_dict = {}
#  try:
#    task_action_id = request.GET.get('task_action_id')
#    print "Searching action"
#    task_action = get_object_or_404(TaskAction, pk=task_action_id)
#    print "Creating manager"
#    manager = ActionManager([task_action])
#    print "Executing manager"
#    action_results = manager.execute()
#    print "Printing results"
#    print str(action_results)
#  except Exception as e:
#    print e
#    print "Unexpected error:", sys.exc_info()[0]
#    return HttpResponse(str(e))
#  response_dict.update({'success': True})
#  return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');

@login_required
def do_action(request):
  print "do_action"
  response_dict = {}
  try:
    model_action_id = request.GET.get('model_action_id')
    model_class_name = request.GET.get('model_class').capitalize()
    model_action_class = get_class('glue.models.' + model_class_name + 'Action')
    print "Searching action"
    model_action = get_object_or_404(model_action_class, pk=model_action_id)
    print "Creating manager"
    manager = ActionManager([model_action])
    print "Executing manager"
    action_results = manager.execute()
    print "Printing results"
    print str(action_results)
  except Exception as e:
    print e
    print "Unexpected error:", sys.exc_info()[0]
    return HttpResponse(str(e))
  response_dict.update({'success': True})
  model_action.finished = True;
  model_action.save()
  return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');


#@login_required
#def update_task_action(request):
#  response_dict = {}
#  try:
#    task_action_id = request.GET.get('task_action_id')
#    enabled = request.GET.get('enabled') == "true"
#    finished = request.GET.get('finished') == "true"
#    print "%s,%s,%s" % (task_action_id, enabled, finished)
#
#    task_action = get_object_or_404(TaskAction, pk=task_action_id)
#    task_action.enabled = enabled
#    task_action.finished = finished
#    task_action.save()
#  
#  except Exception as e:
#    print e
#    print "Unexpected error:", sys.exc_info()[0]
#    return HttpResponse(str(e))
#  response_dict.update({'success': True})
#  return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript');

@login_required
def update_model_action(request):
  response_dict = {}
  try:
    model_action_id = request.GET.get('model_action_id')
    model_class_name = request.GET.get('model_class').capitalize()
    enabled = request.GET.get('enabled') == "true"
    finished = request.GET.get('finished') == "true"
    print "%s,%s,%s" % (model_action_id, enabled, finished)
    
    print "Getting class %s" % model_class_name + 'Action' 
    model_action_class = get_class('glue.models.' + model_class_name + 'Action')
    model_action = get_object_or_404(model_action_class, pk=model_action_id)
    model_action.enabled = enabled
    model_action.finished = finished
    model_action.save()
  
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
    model_id = request.GET.get('instance_id')
    model = get_object_or_404(Component, pk=model_id)
    json_model = serializers.serialize("json", [model])
    project = serializers.serialize("json", [model.project])

    response_dict.update({'component': json_model, 'project': project, 'component_id': model.id, 'project_id': model.project.id})
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
    task_id = request.GET.get('instance_id')
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

  
@login_required
def delete_task(request):
  """
  Mark a task as deleted. The task will actually not be physically removed.
  """
  #response_dict = {}
  try:
    task_id = request.GET.get('instance_id')
    task = get_object_or_404(Task, pk=task_id)
    task.deleted = True
    task.save()
  except Exception as e:
    print e
    print "Unexpected error:", sys.exc_info()[0]
    return HttpResponse(str(e))
  #response_dict.update({'success': True})
  return HttpResponseRedirect('/glue/dashboard/') # Redirect after POST

