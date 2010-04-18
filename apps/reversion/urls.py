from django.conf.urls.defaults import *

from reversion.views import list_revisions
from reversion.views import show_revision
from reversion.views import revert


urlpatterns = patterns('',
                       url(r'list/(?P<club_id>\d+)/$',
                           list_revisions,
                           {'template_name': 'reversion/list.html'},
                           name='list_revisions'),

                       url(r'show/(?P<revision_id>\d+)/$',
                           show_revision,
                           {'template_name': 'reversion/show.html'},
                           name='show_revision'),                           

                       url(r'revert/(?P<revision_id>\d+)/$',
                           revert,
                           name='revert'),                            
)
