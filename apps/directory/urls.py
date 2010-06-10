from django.conf.urls.defaults import *

urlpatterns = patterns('directory.views',
	(r'^$', 'index'),
	(r'^country/(?P<country_name>[a-zA-Z]+)/$', 'country'),
	(r'^(?P<state_usps_name>[a-z]{2})-clubs\.html$', 'state'),
	(r'^club/(?P<club_id>\d+)/(?:(?P<club_urlsafe_title>[\w-]+)\.html)?$', 'club'),
	(r'^club/change/(?P<club_id>\d+)/$', 'change_club'),
	(r'^club/added/(?P<club_id>\d+)/$', 'club_added'),
	(r'^clubs/$', 'clubs'),
	(r'^club/take/(?P<club_id>\d+)/$', 'take_club'),
	(r'^club/add/$', 'add_club'),
 
	(r'^ajax/get-country-cities/$', 'ajax_get_country_cities'),
    
	(r'^tradingmap\.html$', 'tradingmap'),	
)

# urls for admin_views functions
urlpatterns += patterns('directory.admin_views',
	(r'state/(?P<state_id>\d+)/$', 'state_cities'),
	(r'geocoder/$', 'geocoder_proxy'),
	(r'current_state/$', 'get_current_state'),
)
