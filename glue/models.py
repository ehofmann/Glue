from django.db import models
from django.contrib.auth.models import User

path_length = 200

class Project(models.Model):
    name = models.CharField(max_length=30)
    release_list_project_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User)
    brain_baseline = models.CharField(max_length=50, null=True, blank=True)
    modad = models.CharField(max_length=path_length, null=True, blank=True)
    sysad = models.CharField(max_length=path_length, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_fields(self):
        return [(field, field.value_to_string(self)) for field in Project._meta.fields]
    
class Component(models.Model):
    previous_ist_version = models.CharField(max_length=20, null=True, blank=True)
    ist_version = models.CharField(max_length=20)
    ist_name = models.CharField(max_length=20)
    ist_version_created = models.BooleanField(default=False)
    #release_notes_path = models.CharField(max_length=path_length, null=True, blank=True)
    #release_notes_text = models.CharField(max_length=300, null=True, blank=True)
    workspace_dir = models.CharField(max_length=path_length, null=True, blank=True)
    perforce_branch = models.CharField(max_length=50, null=True, blank=True)
    srs_path = models.CharField(max_length=path_length, null=True, blank=True)
    new_srs_name = models.CharField(max_length=50, null=True, blank=True)
    srs_version = models.CharField(max_length=20, null=True, blank=True)
    version_brain_baseline = models.CharField(max_length=50, null=True, blank=True)
    pom_task_id = models.IntegerField(max_length=10, null=True, blank=True)
    tag = models.CharField(max_length=path_length, null=True, blank=True)
    workload = models.IntegerField(max_length=5, null=True, blank=True)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return "%s - %s (%s)" % (self.ist_name, self.ist_version, self.user)
    
    def get_fields(self):
        return [(field, field.value_to_string(self)) for field in Component._meta.fields]
    
class Task(models.Model):
    module_brain_requirement = models.CharField(max_length=50, null=True, blank=True)
    brain_requirement = models.CharField(max_length=50, null=True, blank=True)
    cr_number = models.IntegerField(max_length=10, null=True, blank=True)
    cr_synopsis = models.CharField(max_length=100, null=True, blank=True)
    cr_description = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=200)
    test_description = models.CharField(max_length=200, null=True, blank=True)
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=False)
    component = models.ForeignKey(Component, blank=False)
    pom_task_id = models.IntegerField(null=True, blank=True)
    workload = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    perforce_changelist = models.IntegerField(null=True, blank=True)
    reviewboard_request_id = models.IntegerField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    def __unicode__(self):
        return "Requirement: %s, CR %s, Description: %s (%s)" % (self.brain_requirement, self.cr_number, self.description, self.user)
    
    def get_fields(self):
        return [(field, field.value_to_string(self)) for field in Task._meta.fields]


class Action(models.Model):
    classname = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    model_name = models.CharField(max_length=20, default='task')

    def __unicode__(self):           
        return "Action: %s - %s (%s)" % (self.name, self.description, self.classname)
   
class ModelAction(models.Model):
  action = models.ForeignKey(Action)
  last_execution = models.DateTimeField(null=True)
  finished = models.BooleanField(default=False)
  enabled = models.BooleanField(default=True)
  visible = models.BooleanField(default=True)
  manual = models.BooleanField(default=True)
  nr = models.IntegerField(default=0)
  comment = models.CharField(default="", max_length=100)

  class Meta:
    abstract = True
    
 
class TaskAction(ModelAction):
    task = models.ForeignKey(Task)
    
    def __unicode__(self):           
        return "%s | %s | Task: %s" % (self.task.description, self.action, self.task)
        
class ComponentAction(ModelAction):
    component = models.ForeignKey(Component)

