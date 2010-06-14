from django.conf.urls.defaults import *
from rss.feeds import *

feeds = {
    'site': LatestNews,
    'club': ClubNews,
    'state': StateNews,
    'country': CountryNews
}

urlpatterns = patterns('',

                        url(r'(?P<url>.*)/$',
                            'django.contrib.syndication.views.feed', 
                            {'feed_dict': feeds}, 
                            name="news_feed"),
                           
)
