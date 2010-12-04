from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^webian/', include('webian.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^photos/static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/tola/code/webian/prototypes/photos/webian/src/webian/photos/static'}),
    (r'^photos/', include('photos.urls')),
    (r'^admin/', include(admin.site.urls)),
)
