import re
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
    form = ExtraCommentForm(target_object=target_object, initial=initial_data)	
    return form
   
class ExtraCommentForm(CommentForm):
    def __init__(self, target_object, *argc, **kwargs):
        super(ExtraCommentForm, self).__init__(target_object=target_object, *argc, **kwargs)

    def get_comment_model(self):
        return Comment

    def get_comment_create_data(self):
        data = super(ExtraCommentForm, self).get_comment_create_data()
        return data

    def clean_comment(self):
        """ do not allows '<a>', do not allow 'http://' more then twice        
        """
        comment_ = self.cleaned_data["comment"]
        # <a> tag filter
        if re.compile(r"<\s*a.+>", re.DOTALL).search(comment_):
            raise forms.ValidationError("Please, remove '<a>' tag from comment.")
       
        # more then 2 http:// filter
        matched = re.findall(r"http://", comment_) or []
        if len(matched) > 0:
            raise forms.ValidationError("Do not enter more then 2 http:")
        
        return comment_

class OwnerCommentForm(forms.ModelForm):
    """form where owner of club can change club's comment from other users"""
    class Meta:
        model = Comment
        fields = ("comment",)
