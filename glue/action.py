import glue

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
		):
        self.__model = model
	self.__required_parameters = required_parameters
	self.__provided_parameters = provided_parameters
	self.__name = name
        self.__description = description
    
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


class ManualAction(Action):
    def __init__(self, model):
        Action.__init__(self, model,
			[],
			[],
			"Manual Action",
			"Do the task manual")
        

    def execute(self):
	return ["Skipping manual action: %s" % self.model.action_description]

    
class CreateComponentBrainRequirementAction(Action): 
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
	return ["Creating component brain requirement from module brain requirement: %s" % self.model.action_description]

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


def get_action_names():
	return ['glue.action.CreateComponentBrainRequirementAction']

initialized = False

def init_actions():
	global initialized
	if initialized == False:
		print "init_actions"
		for name in get_action_names():
			print "Action: %s" % name
			
			try:
				a = glue.models.Action.objects.get(classname=name)
				print "Action %s already in db" % name
				print "action description %s" % a.description
			except glue.models.Action.DoesNotExist:
				print "Creating action: %s" % name
			        model = ""	
				a = glue.action.get_class(name)(model)
				print "action description %s" % a.description
				new_action = glue.models.Action(	classname=name, 
								description=a.get_description(), 
								name=a.get_name())
				new_action.save()
	initialized = True

		
