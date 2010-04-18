from django.conf.urls.defaults import *

from news.feeds import LatestNews
from news.views import add
from news.views import change
from news.views import news_list
from news.views import delete_news
from news.views import show

feeds = {
    'sitenews': LatestNews,
}

urlpatterns = patterns('',
                        url(r'list/(?P<club_id>\d+)/$',
                           news_list,
                           {'template_name': 'news/news_list.html'},
                           name='news_list'),
                           
                        url(r'add/(?P<club_id>\d+)/$',
                           add,
                           {'template_name': 'news/change_news_form.html'},
                           name='add_news'),

                        url(r'change/(?P<news_id>\d+)/$',
                           change,
                           {'template_name': 'news/change_news_form.html'},
                           name='change_news'),                          

                        url(r'show/(?P<news_id>\d+)/$',
                           show,
                           {'template_name': 'news/show.html'},
                           name='show_news'),
                           
                        url(r'delete/(?P<news_id>\d+)/$',
                           delete_news,
                           name='delete_news'),
                           
                        url(r'feeds/(?P<url>.*)/$',
                            'django.contrib.syndication.views.feed', 
                            {'feed_dict': feeds}, 
                            name="news_feed"),

                           
)
