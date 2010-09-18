from django.contrib.comments.models import Comment
from extra_comments.forms import ExtraCommentForm

def get_model():
    return Comment

def get_form():
    return ExtraCommentForm
