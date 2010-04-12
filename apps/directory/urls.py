from django.conf.urls.defaults import *

urlpatterns = patterns('directory.views',
	(r'^$', 'index'),
	(r'^(?P<state_usps_name>[a-z]{2})-clubs\.html$', 'state'),
	(r'^club/(?P<club_id>\d+)/(?:(?P<club_urlsafe_title>[\w-]+)\.html)?$', 'club'),
	(r'^club/change/(?P<club_id>\d+)/$', 'change_club'),
	(r'^clubs/$', 'clubs'),    
	(r'^tradingmap\.html$', 'tradingmap'),	
)

# urls for admin_views functions
urlpatterns += patterns('directory.admin_views',
	(r'state/(?P<state_id>\d+)/$', 'state_cities'),
	(r'geocoder/$', 'geocoder_proxy'),
	(r'current_state/$', 'get_current_state'),
)