from django.db import models
from django.contrib.comments.models import Comment
from directory.models import Club

# add short comment to the Comment model	
def get_short_comment(self):
	""" returns slice of comment """
	if len(self.comment) > 10:
		short = "%s..." % self.comment[:10]
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