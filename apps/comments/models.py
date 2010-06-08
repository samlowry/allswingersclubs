import settings

from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.db.models.signals import post_delete
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from directory.models import Club

# add short comment to the Comment model	
def get_short_comment(self):
	""" returns slice of comment """
	if len(self.comment) > 100:
		short = "%s..." % self.comment[:100]
	else:
		short = self.comment
	return short
	
Comment.short_comment = get_short_comment


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

def comment_by_owner(self):
    """returns true if it's club's owner's comment. if not returns false"""

    if not self.content_object.owner:
        # club has no owner
        return False

    if self.content_object.owner == self.user:
        return True
        
    return False
    
Comment.by_owner = comment_by_owner

def was_posted_callback(sender, comment, request, **kwargs):
    """comments_was_posted signal handler. send notification email to the club's owner"""
    if comment.content_type.name == "club":  
        club_owner = comment.content_object.owner
        # has user activated account?
        if (club_owner is not None) and (club_owner.is_active) and (club_owner != comment.user):
            context = {'name': comment.user_name, 'club': comment.content_object, 'site': comment.site, 'comment':comment.comment}
            subject = render_to_string("comments/subject.txt", context)
            message = render_to_string("comments/message.txt", context)
            club_owner.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

def club_pd_callback(sender, instance, **kwargs):
    """ club post delete callback. deletes club's comments """
    Comment.objects.for_model(instance).delete()

    
post_delete.connect(club_pd_callback, sender=Club)
comment_was_posted.connect(was_posted_callback, sender=Comment)