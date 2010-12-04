from django.conf.urls.defaults import *

urlpatterns = patterns('photos.views',
    (r'^$', 'index'),
    (r'^(?P<photo_id>\d+)/$', 'detail'),
)