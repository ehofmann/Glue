from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    release_list_project_name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.release_list_project_name
    
class Component(models.Model):
    previous_ist_version = models.CharField(max_length=20)
    ist_version = models.CharField(max_length=20)
    ist_name = models.CharField(max_length=20)
    release_notes_path = models.CharField(max_length=50)
    workspace_dir = models.CharField(max_length=50)
    perforce_branch = models.CharField(max_length=50)
    srs_path = models.CharField(max_length=100)
    new_srs_name = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    def __unicode__(self):
        return "%s - %s (%s)" % (self.ist_name, self.ist_version, self.user)
    
class Task(models.Model):
    brain_requirement = models.CharField(max_length=30)
    cr_number = models.IntegerField(max_length=10)
    description = models.CharField(max_length=100)
    finished = models.BooleanField()
    user = models.ForeignKey(User)
    component = models.ForeignKey(Component)
    def __unicode__(self):
        return "Requirement: %s, CR %s, Description: %s (%s)" % (self.brain_requirement, self.cr_number, self.description, self.user)

#class Action(models.Model):
    #name = models.CharField(max_length=20)
    #description = models.CharField(50)
    #last_execution = models.DateTimeField()
    