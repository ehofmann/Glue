from django.conf.urls.defaults import *
from django.contrib.auth import views
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^glue/', include('Glue.glue.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^(glue/)accounts/login(/)$', 'django.contrib.auth.views.login'),
    (r'^(glue/)accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', ),
    (r'^accounts/profile/$', 'django.contrib.auth.views.login'),
    (r'^accounts/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': "%s/static" % settings.project_dir}),
)
