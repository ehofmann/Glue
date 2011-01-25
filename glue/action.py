import glue

class Action():
    def __init__(self, model):
        self.model = model
    
    def __unicode__(self):
        return self.model.__unicode__()

class ManualAction():
    def __init__(self, model):
        Action.__init__(self, model)


class ActionFactory():
    def __init__(self, model):
        self.model = model
        
    def createAction(self):        
        classname = model.classname
        action = globals()[classname]
        return action
            
            
        