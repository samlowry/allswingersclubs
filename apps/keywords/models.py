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
    def save(self):
        """ saves model and removes elder """
        super(Keyword, self).save()
        self.sites.add(Site.objects.get_current())
        super(Keyword, self).save()
        old = Keyword.objects.all().order_by("-id")[settings.MAX_STACK_LENGTH:]
        for word in old:
            word.delete()
            
