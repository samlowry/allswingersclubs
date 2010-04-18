from django.contrib.syndication.feeds import Feed
# works only for django before 1.2
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from news.models import News


class LatestNews(Feed):
    title = "site news"
    link = "/sitenews/"
    description = "News about clubs"
    
    def items(self):
        return News.objects.order_by('-created')[:10]
