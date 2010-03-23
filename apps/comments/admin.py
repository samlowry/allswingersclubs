from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment


# extending generic Comments application for adding short comments
# unregister Comment model admin

try:
    admin.site.unregister(Comment)
except:
    pass

class ExtendedCommentsAdmin(CommentsAdmin):
	# new list_display with short_comment
    # Comment doesn't have short_comment, it adds in the directory.models
	list_display = ('name', 'object_pk', 'ip_address', 'club_url', 'submit_date', 'short_comment', 'is_public', 'is_removed', )

admin.site.register(Comment, ExtendedCommentsAdmin)