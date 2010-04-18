from django.contrib.comments.forms import CommentForm
from django import forms
from django.contrib.comments.models import Comment

def get_comment_form(request, target_object):
	""" init form with values from request and returns form """
	initial_data = {}
	if request.user.is_anonymous():
		initial_data["name"] = request.session.get("poster_name", "")
		initial_data["email"] = request.session.get("poster_email", "")
		initial_data["url"] = request.session.get("poster_url", "")
	
	# TO DO add here authenticated user's processing
	
	form = CommentForm(target_object=target_object, initial=initial_data)	
	return form
    
class OwnerCommentForm(forms.ModelForm):
    """form where owner of club can change club's comment from other users"""
    class Meta:
        model = Comment
        fields = ("comment",)