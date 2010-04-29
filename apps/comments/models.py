from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted

from directory.models import Club
import settings

# add short comment to the Comment model	
def get_short_comment(self):
	""" returns slice of comment """
	if len(self.comment) > 100:
		short = "%s..." % self.comment[:100]
	else:
		short = self.comment
	return short
	
Comment.short_comment = get_short_comment

# add club homepage to the comments list
# def get_club_homepage(self):
#	""" get club by Comment.object_pk and returns it homepage """
#	if self.content_type.name == "club":
#		try:
#			club = Club.objects.get(id=self.object_pk)
#		except club.DoesNotExist:
#			return "-"
#	return club.homepage_url()
#	
# get_club_homepage.allow_tags = True
# Comment.club_homepage = get_club_homepage
# ##### uncomment and add club_homepage to the 
# ##### comments.admin.ExtendedCommentAdmin.list_display

# add club url to the comments list
def get_club_url(self):
	""" get club by Comment.object_pk and returns it homepage """
	if self.content_type.name == "club":
		try:
			club = Club.objects.get(id=self.object_pk)
		except club.DoesNotExist:
			return "-"
	return "<a href='%s'>%s</a>" % (club.get_absolute_url(), club.name)
	
get_club_url.allow_tags = True
Comment.club_url = get_club_url

def get_poster_url(self):
	""" returns html formatted homepage url """
	if self.url == '':
		return ''
	return "<a href='%(url)s'>#</a>" % {"url": self.url}
get_poster_url.allow_tags = True
Comment.poster_url = get_poster_url

def was_posted_callback(sender, comment, request, **kwargs):
    """comments_was_posted signal handler. send notification email to the club's owner"""
    if comment.content_type.name == "club":  
        club_owner = comment.content_object.owner
        # has user activated account?
        if (club_owner is not None) and (club_owner.is_active):
            subject = "comment"
            message = "%s has commented %s" % (comment.user_name, comment.content_object.name)
            club_owner.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

comment_was_posted.connect(was_posted_callback, sender=Comment)