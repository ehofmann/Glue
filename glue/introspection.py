import action
from inspect import getmembers, isclass


def get_action_class_names():
	action_children = []
	action_classes = getmembers(action, isclass)
	for (class_name, action_class) in action_classes:
		if -1 != str(action_class.__bases__).find("glue.action.Action"):
			action_children.append(class_name)
	print str(action_children)
	return action_children

