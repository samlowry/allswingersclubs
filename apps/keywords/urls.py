from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', 'keywords.views.search'),
)

