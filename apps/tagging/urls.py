from django.conf.urls.defaults import *

from tagging.views import state_clubs
from tagging.views import country_clubs

urlpatterns = patterns('',
                        url(r'usa/(?P<usps>[a-zA-Z]{2})/(?P<tag_name>[a-zA-Z0-9-]*)/$',
                       #url(r'usa.*/$',
                           state_clubs,
                           {'template_name': 'tagging/region_clubs.html'},
                           name='state_clubs'), 

                        url(r'(?P<country_name>[a-zA-Z0-9-_]*)/(?P<tag_name>[a-zA-Z0-9-]*)/$',
                            country_clubs,
                            {'template_name': 'tagging/region_clubs.html'},
                            name='country_clubs'),
)
