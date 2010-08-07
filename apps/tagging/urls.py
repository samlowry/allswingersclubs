from django.conf.urls.defaults import *

from tagging.views import clubs_by_tag
from tagging.views import clubs_by_land

urlpatterns = patterns('',
                       url(r'tag/(?P<tag_name>[a-zA-Z0-9-]*)/$',
                           clubs_by_tag,
                           {'template_name': 'tagging/tag_clubs.html'},
                           name='clubs_by_tag'), 

                        url(r'(?P<state_name>[a-zA-Z0-9-_]*)/(?P<city_name>[a-zA-Z0-9-_]*)/$',
                            clubs_by_land,
                            {'template_name': 'tagging/clubs_by_land.html'},
                            name='clubs_by_land'),
)
