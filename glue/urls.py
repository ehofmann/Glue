from django.conf.urls.defaults import *

urlpatterns = patterns('glue.views',
    (r'^$', 'user_dashboard'),
    (r'^dashboard/$', 'user_dashboard'),
    (r'^show_model/(?P<model>.+)/(?P<instance_id>\d+)/$', 'show_model'),
    (r'^create_action/$', 'create_action'),
    (r'^create_(?P<modelType>.+)/$', 'create_model'),
    (r'^do_action/$', 'do_action'),
    (r'^update_model_action/$', 'update_model_action'),
    (r'^get_task/$', 'get_task'),
    (r'^get_component/$', 'get_component'),
    (r'^delete_task/$', 'delete_task'),
)
