import glue, time
from glue.introspection import get_action_class_names
from glue.models import Task,TaskAction

def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
	m = getattr(m, comp)            
    return m 


class Action():
    def __init__(self,
		 model,
		 required_parameters,
		 provided_parameters,
		 name,
		 description,
     model_name='task',
     is_manual = True,
		):
      self.__model = model
      self.__required_parameters = required_parameters
      self.__provided_parameters = provided_parameters
      self.__name = name
      self.__description = description
      self.__model_name = model_name
      self.__is_manual = is_manual

    def get_model(self):
	return self.__model
    model = property(get_model)
    
    def __unicode__(self):
        return self.model.__unicode__()

    def get_description(self):
        return self.__description	
    description = property(get_description)	
    
    def get_name(self):
        return self.__name	
    name = property(get_name)	
    
    def get_required_parameters(self):
        return self.__required_parameters
    required_parameters = property(get_required_parameters)	
    
    def get_provided_parameters(self):
        return self.__provided_parameters
    provided_parameters = property(get_provided_parameters)	

    def get_model_name(self):
        return self.__model_name	
    model_name = property(get_model_name)	

    def execute(self):
	return [self.__model.action.description]

    def is_manual(self):
      return self.__is_manual

"""
Component tasks
"""
    
class CreateIstComponentVersion(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_ist_version", "Component_previous_ist_version"], 
			[],
			"IST version",
			"Creates the IST component version, if it does not exist yet",
      model_name='component',
			)

class CreateParamDbVersion(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_ist_version", "Component_previous_ist_version"], 
			[],
<<<<<<< HEAD
			"Param Db",
			"Creates the Param Db version, if it does not exist yet",
=======
			"IST version",
			"Creates the Param db version, if it does not exist yet",
      model_name='component',
>>>>>>> ffe10cfa876faba0cb2e6e2b0ddc0dfb04698cb2
			)

class UpdateReleaseListVersion(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_ist_version", "Project_release_list_project_name"], 
			[],
			"Release list version",
			"Updates the release list with the component version",
      model_name='component',
			)

class UpdateReleaseListSrsVersion(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_srs_version"], 
			[],
			"Release list SRS version",
			"Updates the release list with the component SRS version",
      model_name='component',
			)

class CreateBrainComponentVersion(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_ist_version", "Component_previous_ist_version"], 
			["Component_version_brain_baseline"],
			"Brain component version baseline",
			"Creates the brain component version baseline, if it does not exist yet",
      model_name='component',
			)



class CreateNewSrs(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_srs_path", "Component_new_srs_name"], 
			[],
			"Create New SRS",
			"Creates a new SRS file from the previous version and updates the properties. Adds a history etnrtry with the differences of current and previous component version in brain.",
      model_name='component',
			)

class SendSrsForReview(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_srs_path", "Component_new_srs_name"], 
			[],
			"SRS PI review",
			"Send the SRS for review to PI.",
      model_name='component',
			)

class CreatePomTaskToCreateComponent(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_ist_name", "Component_ist_version"], 
			["Component_pom_task_id"],
			"POM task to create component",
			"POM task to create component",
      model_name='component',
			)

class CreateTag(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Component_ist_name", "Component_ist_version"], 
			["Component_tag"],
			"Create Tag",
			"Tags the component version in perforce",
      model_name='component',
			)

class ComponentWorkloadFinalized(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			[], 
			["Component_workload"],
			"Finalize component workload",
			"Finalize the workload related to the component creation",
      model_name='component',
			)

class CreateIstPackage(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			required_parameters = ["Component_ist_name", "Component_ist_version", "Component_previous_ist_version"], 
			provided_parameters = ["ist_package_id"],
			name                = "Create IST package",
			description         = "Creates the package of the version in IST, updates the release notes, the package file link and the compabilities.",
      model_name          = 'component'
			)

#class UpdateSrsBaseline(Action):
#    def __init__(	self, 
#			model,
#	):
#        Action.__init__(self, 
#			model,
#			["Component_version_brain_baseline", "Component_release_notes_path", "Component_new_srs_name"], 
#			[],
#			"Update SRS baseline",
#			"Updates all baseline references to the new component baseline.",
#			)

#class UpdateSrsHistory(Action):
#    def __init__(	self, 
#			model,
#	):
#        Action.__init__(self, 
#			model,
#			["Component_version_brain_baseline", "Component_release_notes_path", "Component_new_srs_name"], 
#			[],
#			"Update SRS history",
#			"Updates the SRS history.",
#			)

"""
Task actions
"""

class CreatePomTask(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_cr_number", "Task_cr_description", "Task_cr_synopsis"], 
			["Task_pom_task_id"],
			"Create POM task",
			"Creates a task in POM",
			)

class CreateComponentBrainRequirement(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_module_brain_requirement", "Project_brain_baseline","Component_version_brain_baseline"], 
			["Task_brain_requirement"],
			"Brain Requirement",
			"Create Brain requirment of component",
			)
    
    def execute(self):
	return ["Creating component brain requirement from module brain requirement: %s" % self.model.action.description]

class CreateCrFromRequirement(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_brain_requirement", "Component_ist_version", "Component_ist_name"], 
			["Task_cr_number", "Task_cr_description", "Task_cr_synopsis"],
			"Create Cr",
			"Creates a CR targetting the ist version of the component. If the cr synopsis or description is not available yet, then they are copied from the requirement, if it exists.",
			)

class AddRequirementToSRS(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_brain_requirement"], 
			[],
			"Add requirement to SRS",
			"Adds the requirement to the SRS.",
			)


class PullIstRecordData(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_cr_number"], 
			["Task_cr_description", "Task_cr_synopsis"],
			"Pull CR/PR data",
			"Retrieves the CR/PR description and synopsis from ist",
			)

class FinishIstRecord(Action): 
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_cr_number", "perforce_changelist"], 
			[],
			"Finish CR/PR",
			"Adds the changelists to the CR/PR response. Sets version to corrected.",
			)


class FinishPomTask(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_pom_task_id", "Task_workload"],
			[],
			"Finish POM task",
			"Updates POM task with workload and closes it",
			)

class CreateAndSubmitChangelist(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			["Task_cr_number", "Component_perforce_branch"], 
			["Task_perforce_changelist"],
			"Changelist",
			"Creates and submites the changelist for the task.",
			)

class BrainRequirementNote(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			required_parameters =   ["Task_cr_number", "Task_brain_requirement"], 
			provided_parameters =   [""],
			name = 			"Brain Requirement Note",
			description = 		"Updates the brain requirement's node with the CR number",
			)

class CreateReviewRequest(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			required_parameters =   ["Task_perforce_changelist", "Task_cr_number", "Task_test_description"], 
			provided_parameters =   ["Task_reviewboard_request_id"],
			name = 			"Create review request",
			description = 		"Creates a reviewboard request from the changelist",
			)

class ReviewFinished(Action):
    def __init__(	self, 
			model,
	):
        Action.__init__(self, 
			model,
			required_parameters =   ["Task_reviewboard_request_id"], 
			provided_parameters =   [""],
			name = 			"Review Finished",
			description = 		"Indicates that the review has been finished and the ship it, has been granted.",
			)


class ActionFactory():
        
    def createAction(self, model):        
        classname = model.action.classname
	print "createAction for class %s" % classname
        #action = globals()[classname]
	action = get_class(classname)(model)
	#action = ManualAction(model)
        return action

            
class ActionManager():
	def __init__(self, task_actions):
		self.task_actions = task_actions
		self.factory = ActionFactory()

	def execute(self):
		results = {}
		for task_action in self.task_actions:
			action = self.factory.createAction(task_action)
			result = action.execute()
			results[task_action.id] =  result
			
		return results

initialized = False

def init_actions():
  global initialized
  if initialized == False:
    print "init_actions"
    for name in get_action_class_names():
      name = "glue.action.%s" % name
      print "Action: %s" % name

      try:
        existing_action = glue.models.Action.objects.get(classname=name)
        print "Action %s already in db" % name
        print "action description %s" % existing_action.description
        a = glue.action.get_class(name)(existing_action)
        existing_action.description = a.get_description()
        existing_action.name = a.get_name()
        existing_action.model_name = a.get_model_name()
        existing_action.manual = a.is_manual()
        existing_action.save()
      except glue.models.Action.DoesNotExist:
        print "Creating action: %s" % name
        model = ""	
        a = glue.action.get_class(name)(model)
        print "action description %s" % a.description
        new_action = glue.models.Action(	classname=name, 
                description=a.get_description(), 
                name=a.get_name(),
                model_name = a.get_model_name()
                )
        new_action.save()
        model_class = get_class('glue.models.' + new_action.model_name.capitalize())
        for instance in model_class.objects.all():
          params = {'action': new_action, new_action.model_name: instance}
          model_action_class = get_class('glue.models.' + new_action.model_name.capitalize() + 'Action')
          new_task_action = model_action_class(**params)
          new_task_action.save()
	initialized = True

		
