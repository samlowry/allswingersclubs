from django.contrib.syndication.feeds import Feed
# works only for django before 1.2
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from news.models import News
from directory.models import Club
from directory.models import State


class LatestNews(Feed):
    title = "site news"
    link = "/sitenews/"
    description = "News about clubs"
    
    def items(self):
        return News.objects.order_by('-created')[:10]
        
class ClubNews(Feed):

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
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        # get state usps name from bits [0]            
        if bits[0].endswith("-clubs.html"):
            usps = bits[0][:2] 
        else:
            raise ObjectDoesNotExist
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
        