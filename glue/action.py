import glue

class Action():
    def __init__(self, model):
        self.model = model
    
    def __unicode__(self):
        return self.model.__unicode__()

class ManualAction():
    def __init__(self, model):
        Action.__init__(self, model)

    def execute():
	return ["Skipping manual action: %s" % self.model.action_description]


class ActionFactory():
        
    def createAction(self, model):        
        classname = model.action.classname
        action = globals()[classname]
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


	
