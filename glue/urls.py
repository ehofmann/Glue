from django.conf.urls.defaults import *

urlpatterns = patterns('glue.views',
    (r'^$', 'user_dashboard'),
    (r'^dashboard/$', 'user_dashboard'),
    (r'^task/(?P<task_id>\d+)/$', 'task'),
    (r'^create_task/$', 'create_task'),
    (r'^create_component/$', 'create_component'),
    (r'^create_project/$', 'create_project'),
    (r'^do_action/$', 'do_action'),
    (r'^update_task_action/$', 'update_task_action'),
    (r'^get_task/$', 'get_task'),
)
