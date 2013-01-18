from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'data_manager.views.directupload', name='directupload'),
)