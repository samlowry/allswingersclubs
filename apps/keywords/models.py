import datetime
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

import settings
  

class Keyword(models.Model):
    text = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.datetime.now)
    sites = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')
    def save(self, site=None):
        """ saves model and removes elder. site - is site object which to keyword"""
        # checking keyword existance
        if site is None:
            site = Site.objects.get_current()
        kws = Keyword.objects.filter(text=self.text, sites=site)
        if kws.count() == 0:
            super(Keyword, self).save()
            self.sites.add(site)
            old = Keyword.on_site.all().order_by("-id")[settings.MAX_STACK_LENGTH:]
            for word in old:
                word.delete()
    
    def query_string(self):
        return self.text.replace(" ", "+")

class IsOnForCurrentSite(models.Manager):
    def enabled(self):
        is_on = False
        try:
            is_on = Site.objects.get_current().keywordstate.is_on
        except KeywordState.DoesNotExist:
            pass
        return is_on
        

class KeywordState(models.Model):
    is_on = models.BooleanField(default=False)
    site = models.OneToOneField(Site)
    
    # managers
    objects = models.Manager()
    state = IsOnForCurrentSite()



