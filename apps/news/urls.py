from django.conf.urls.defaults import *

from news.views import add
from news.views import change

urlpatterns = patterns('',
                       url(r'add/(?P<club_id>\d+)/$',
                           add,
                           {'template_name': 'news/change_news_form.html'},
                           name='add_news'),

                       url(r'change/(?P<news_id>\d+)/$',
                           change,
                           {'template_name': 'news/change_news_form.html'},
                           name='change_news'),                          

)
