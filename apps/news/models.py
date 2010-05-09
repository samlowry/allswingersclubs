import datetime
from django.db import models
from directory.models import Club

# Create your models here.
class News(models.Model):
    club = models.ForeignKey(Club, db_index=True)
    created = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    changed = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    text = models.TextField() 

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        
    def __unicode__(self):
        return "%s..." % self.text[:20]
        
    def save(self):
        self.changed = datetime.datetime.now()
        super(News, self).save()
        
    def get_absolute_url(self):
        return "/news/show/%s/" % self.id