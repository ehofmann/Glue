from django.conf.urls.defaults import *

urlpatterns = patterns('glue.views',
    (r'^$', 'user_dashboard'),
    (r'^task/(?P<task_id>\d+)/$', 'task'),
    #(r'^logout/$', 'logout_user'),
    #(r'^login/next=(?P<next_url>.+)$', 'login'),
)