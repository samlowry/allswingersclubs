import datetime

from django.db import models
from django.db.models import Max

from directory.models import Club
from django.db.models.signals import post_save
from django.core import serializers

# Create your models here.
class ClubReversion(models.Model):
    club = models.ForeignKey(Club, db_index=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    serialized_data = models.TextField() # json format
    comment = models.TextField(default="") # 20:05
    
    def __unicode__(self):
        return "%s (%s)" % (self.club, self.created)
        
    def get_reverted(self):
        club = serializers.deserialize("json", self.serialized_data).next().object
        return club
    reverted = property(get_reverted)
        
    def get_absolute_url(self):
        return "/reversions/show/%s" % self.id
    
    def revert(self):
        """reverts club to current revision"""
        # get club object from serialized data
        club = self.get_reverted()
        # save reverted club
        club.save()
        
def club_postsave_callback(sender, **kwargs):
    """serialize club object, and saves it"""
    club = kwargs["instance"]
    # get previous revision
    prev_revisions = ClubReversion.objects.filter(club=club).order_by("-created")
    prev_data = ""
    if prev_revisions.count() > 0:
        prev_data = prev_revisions[0].serialized_data
        
    # get current object serialization data
    current_data = serializers.serialize("json", [club])
    if prev_data != current_data:
        # print "club changed. save revision"
        rev = ClubReversion()
        rev.club = club
        rev.serialized_data = current_data
        rev.save()
    
post_save.connect(club_postsave_callback, sender=Club)