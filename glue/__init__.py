#def init_parameters():
#	# initialise the parameters table
#	parameter_names = []
#	for f in models.Task._meta.fields:
#		parameter_names.append("Task.%s" % f.name)
#	for f in models.Component._meta.fields:
#		parameter_names.append("Component.%s" % f.name)
#	for f in models.Project._meta.fields:
#		parameter_names.append("Project.%s" % f.name)
#
#	for param in parameter_names:
#		try:
#			p = models.Parameter.objects.get(name = param)
#			print "%s does already exist" % param
#		except models.Parameter.DoesNotExist as e:
#			print  "%s does not exist, adding it to Parameter" % param
#			p = models.Parameter(name = param)
#			p.save()


#def init_actions():
#	print "init_actions"
#	for name in action.get_action_names():
#		
#		try:
#			a = Action.objects.get(classname=name)
#			print "Action %s already in db" % name
#		except Action.DoesNotExist:
#			print "Creating action: %s" % name
#			a = glue.action.get_class(name)
#			new_action = models.Action(	classname=name, 
#							description=action.description, 
#							name=action.name)
#			new_action.save()
#
#try:
#	#init_parameters()
#	print "Init glue"
#	init_actions()
#except Exception as e:
#	print "Exception: " + str(e) 
#
