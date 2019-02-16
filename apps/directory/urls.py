# import warnings
# warnings.simplefilter('error', DeprecationWarning)

from django.conf.urls.defaults import patterns
from django.views.generic.list import ListView
from directory.models import Club
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

handler404 = 'directory.views.view_404'

urlpatterns = patterns(
    'directory.views',
    (r'^$', 'index'),
    (r'^analytics\.html$', 'analytics'),
    (r'^country/(?P<slug>[a-zA-Z -]+)/$', 'country'),
    (r'^(?P<state_usps_name>[a-z]{2})-clubs\.html$', 'state'),
    (r'^city/(?P<city_id>\d+)/(?:(?P<city_urlsafe_name>[\w-]+)-clubs\.html)?$', 'city'),
    (r'^(?P<state_usps_name>[a-z]{2})-hookups\.html$', 'state2'),
    (r'^club/(?P<club_id>\d+)/(?:(?P<club_urlsafe_title>[\w-]+)\.html)?$', 'club'),
    (r'^club/change/(?P<club_id>\d+)/$', 'change_club'),
    (r'^club/added/(?P<club_id>\d+)/$', 'club_added'),
    (r'^clubs/$', 'clubs'),
    (r'^club/take/(?P<club_id>\d+)/$', 'take_club'),
    (r'^club/add/$', 'add_club'),
    (r'^hookup/(?P<hookup_id>\d+)/(?:(?P<hookup_urlsafe_title>[\w-]+)\.html)?$', 'hookup'),
    (r'^ajax/get-country-cities/$', 'ajax_get_country_cities'),
    (r'^tradingmap\.html$', 'tradingmap'),
    (r'^csvmap\.csv$', 'csvmap'),
)

# redirect url for club
urlpatterns += patterns('', (r'^shorturl/(?P<object_id>\d+)/$', ListView.as_view, {
    'queryset': Club.objects.all(),
    'template_name': 'directory/shorturl.html',
    'template_object_name': 'club'
}),
)

# urls for admin_views functions
urlpatterns += patterns(
    'directory.admin_views',
    (r'state/(?P<state_id>\d+)/$', 'state_cities'),
    (r'geocoder/$', 'geocoder_proxy'),
    (r'current_state/$', 'get_current_state'),
)

if settings.DEBUG:
    # add one of these for every non-static root you want to serve
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # this take cares of static media (i.e. bundled in apps, and specified in settings)
    urlpatterns += staticfiles_urlpatterns()
