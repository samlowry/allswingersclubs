from django.conf.urls.defaults import *

urlpatterns = patterns('directory.views',
	(r'^$', 'index'),
	(r'^(?P<state_usps_name>[a-z]{2})-clubs\.html$', 'state'),
	(r'^club/(?P<club_id>\d+)/(?:(?P<club_urlsafe_title>[\w-]+)\.html)?$', 'club'),
)

