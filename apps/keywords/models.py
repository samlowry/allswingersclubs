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
        super(Keyword, self).save()
        if site is None:
            site = Site.objects.get_current()
        self.sites.add(site)
        old = Keyword.objects.all().order_by("-id")[settings.MAX_STACK_LENGTH:]
        for word in old:
            word.delete()
    
    def query_string(self):
        return self.text.replace(" ", "+")
