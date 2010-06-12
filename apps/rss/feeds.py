from django.contrib.syndication.feeds import Feed
# works only for django before 1.2
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from news.models import News
from directory.models import *


class LatestNews(Feed):
    site = Site.objects.get_current()
    title = "%s news" % site.name
    link = "/"
    description = "News of all clubs, listed in %s directory" % site.name
    
    title_template = "feeds/news_title.html"
    description_template = "feeds/news_description.html"
    
    def items(self):
        return News.objects.order_by('-created')[:10]

class ClubNews(Feed):    
    title_template = "feeds/news_title.html"
    description_template = "feeds/news_description.html"
    
    def title(self, obj):
        return "%s news feed" % obj.name
    
    def get_object(self, bits):
        """returns feed object that is using to filter items"""
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Club.objects.get(id__exact=bits[0])
    
    def description(self, obj):
        return "%s news feed" % obj.name
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()
    
    def items(self, obj):
        return News.objects.filter(club__id__exact=obj.id).order_by('-created')[:10]
        

class StateNews(Feed):
    
    title_template = "feeds/news_title.html"
    description_template = "feeds/news_description.html"
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        usps = bits[0]
        return State.objects.get(usps_name__iexact=usps)
    
    def title(self, obj):
        return "%s state feed" % obj.name
    
    def description(self, obj):
        return "%s state feed" % obj.name
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()
    
    def items(self, obj):
        return News.objects.filter(club__state__id__exact=obj.id).order_by('-created')[:10]
        
        
        
class CountryNews(Feed):
    
    title_template = "feeds/news_title.html"
    description_template = "feeds/news_description.html"
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        country_name = bits[0]
        return Country.objects.get(name=country_name)
    
    def title(self, obj):
        return "%s country feed" % obj.name
    
    def description(self, obj):
        return "%s country feed" % obj.name
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()
    
    def items(self, obj):
        return News.objects.filter(club__city__country__id=obj.id).order_by('-created')[:10]
        
