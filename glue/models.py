from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=30)
    release_list_project_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User)
    brain_baseline = models.CharField(max_length=50, null=True, blank=True)
    modad = models.CharField(max_length=100, null=True, blank=True)
    sysad = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_fields(self):
        return [(field, field.value_to_string(self)) for field in Project._meta.fields]
    
class Component(models.Model):
    previous_ist_version = models.CharField(max_length=20, null=True, blank=True)
    ist_version = models.CharField(max_length=20, null=True, blank=True)
    ist_name = models.CharField(max_length=20, null=True, blank=True)
    release_notes_path = models.CharField(max_length=50, null=True, blank=True)
    release_notes_text = models.CharField(max_length=100, null=True, blank=True)
    workspace_dir = models.CharField(max_length=50, null=True, blank=True)
    perforce_branch = models.CharField(max_length=50, null=True, blank=True)
    srs_path = models.CharField(max_length=100, null=True, blank=True)
    new_srs_name = models.CharField(max_length=20, null=True, blank=True)
    srs_version = models.CharField(max_length=20, null=True, blank=True)
    version_brain_baseline = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    
    
    def __unicode__(self):
        return "%s - %s (%s)" % (self.ist_name, self.ist_version, self.user)
    
    def get_fields(self):
        return [(field, field.value_to_string(self)) for field in Component._meta.fields]
    
class Task(models.Model):
    module_brain_requirement = models.CharField(max_length=30, null=True, blank=True)
    brain_requirement = models.CharField(max_length=30, null=True, blank=True)
    cr_number = models.IntegerField(max_length=10, null=True, blank=True)
    cr_synopsis = models.CharField(max_length=100, null=True, blank=True)
    cr_description = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    component = models.ForeignKey(Component)
    pom_task_id = models.IntegerField(null=True, blank=True)
    workload = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    perforce_changelist = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
        return "Requirement: %s, CR %s, Description: %s (%s)" % (self.brain_requirement, self.cr_number, self.description, self.user)
    
    def get_fields(self):
        return [(field, field.value_to_string(self)) for field in Task._meta.fields]


#class Parameter(models.Model):
#    name = models.CharField(max_length=30, unique=True)
#
#    def __unicode__(self):
#        return self.name     

class Action(models.Model):
    classname = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    #required_parameters = models.ManyToManyField(Parameter, related_name="required_parameters_relation")
    #provided_parameters = models.ManyToManyField(Parameter, related_name="provided_parameters_relation")

    def __unicode__(self):           
        return "Action: %s - %s (%s)" % (self.name, self.description, self.classname)
    
class TaskAction(models.Model):
    action = models.ForeignKey(Action)
    task = models.ForeignKey(Task)
    last_execution = models.DateTimeField(null=True)
    finished = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    #before_development = models.BooleanField(default=True)
    #action_description = models.CharField(max_length=50, default="")
    
    def __unicode__(self):           
        return "%s | %s | Task: %s" % (self.task.description, self.action, self.task)
        
