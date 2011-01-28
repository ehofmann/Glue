from django.conf.urls.defaults import *

urlpatterns = patterns('glue.views',
    (r'^$', 'user_dashboard'),
    (r'^dashboard/$', 'user_dashboard'),
    (r'^task/(?P<task_id>\d+)/$', 'task'),
    (r'^show_task_actions/(?P<task_id>\d+)/$', 'show_task_actions'),
    (r'^show_task_action_table/(?P<task_id>\d+)/$', 'show_task_action_table'),
    (r'^create_task/$', 'create_task'),
    (r'^create_component/$', 'create_component'),
    (r'^create_project/$', 'create_project'),
    (r'^show_actions_before/(?P<task_id>\d+)/$', 'show_actions_before'),
    (r'^do_actions/(?P<task_id>\d+)/(?P<when>[a-z]+)/$', 'do_actions'),
    (r'^do_action/$', 'do_action'),
    (r'^update_task_action/$', 'update_task_action'),
)
