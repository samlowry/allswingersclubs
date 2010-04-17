import datetime

from django.db import models
from directory.models import Club
from django.db.models.signals import post_save
from django.core import serializers

# Create your models here.
class ClubReversion(models.Model):
    club = models.ForeignKey(Club, db_index=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    serialized_data = models.TextField()
    comment = models.TextField() # 20:05
    
    def __unicode__(self):
        return "%s (%s)" % (self.club, self.created)
        
def club_postsave_callback(sender, **kwargs):
    pass
    
post_save.connect(club_postsave_callback, sender=Club)