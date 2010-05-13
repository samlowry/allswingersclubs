import datetime
from django.db import models
from django.contrib.auth.models import User
# from django.core.signals import post_save

from directory.models import Club

# Create your models here.
STATUS_CHOICES = ((1, "New"), (2, "Checked"))


class ClubCapture(models.Model):
    user = models.ForeignKey(User)
    club = models.ForeignKey(Club)
    created = models.DateTimeField(default=datetime.datetime.now)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    comment = models.TextField(default="", blank=True)

    def __unicode__(self):
        return "%s captured %s" % (self.user, self.club)
    
    
    def club_admin_url(self):
        return "<a href='/admin/directory/club/%s/' title='Show club'>%s</a>" % (self.club.id, self.club)
    club_admin_url.allow_tags = True

    club_admin_url.admin_order_field = "club"
   
