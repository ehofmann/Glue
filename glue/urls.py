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
    #(r'^logout/$', 'logout_user'),
    #(r'^login/next=(?P<next_url>.+)$', 'login'),
)