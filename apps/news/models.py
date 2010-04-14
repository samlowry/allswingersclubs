import datetime
from django.db import models
from directory.models import Club

# Create your models here.
class News(models.Model):
    club = models.ForeignKey(Club, db_index=True)
    created = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    changed = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    text = models.TextField() 

    def __unicode__(self):
        return "%s..." % self.text[:20]
        
    def save(self):
        self.changed = datetime.datetime.now()
        super(News, self).save()