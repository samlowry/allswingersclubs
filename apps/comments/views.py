from django.contrib.comments.views.comments import post_comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from extra_comments.forms import OwnerCommentForm
from directory.models import Club


@require_POST
def post_wrapper(request, next=None):
	""" saves user's data from request to the session and call comment's post_comment function """
	if request.method == 'POST': # If the form has been submitted...
		data = request.POST.copy()
		poster_name = data.get("name", "")
		poster_email = data.get("email", "")
		poster_url = data.get("url", "")
		
		# saving poster_name, poster_email and poster_url
		# to the session. it's not the same as the django users,
		# it's just not authenticated users who post comments
		request.session["poster_name"] = poster_name
		request.session["poster_email"] = poster_email
		request.session["poster_url"] = poster_url
	if not next:
		next = request.META['HTTP_REFERER']
	return post_comment(request, next)
	
@login_required
def comments_list(request, template_name="comments/list.html"):
    """shows comments of owner's clubs"""
    context = RequestContext(request)
    club_type = ContentType.objects.get(app_label="directory", model="club")
    comments = Comment.objects.filter(content_type=club_type)
    all_clubs_comments = Comment.objects.for_model(Club)
    owner_clubs_comments = all_clubs_comments.filter(object_pk__in=Club.objects.filter(owner=request.user))
    context["comments"] = owner_clubs_comments
    return render_to_response(template_name, context)
    
@login_required
def comment_change(request, comment_id, template_name="comments/change_form.html"):
    """shows comments of owner's clubs"""
    context = RequestContext(request)
    comment = get_object_or_404(Comment, id=comment_id)
    comment_club = Club.objects.get(id=comment.object_pk)
    if comment_club.owner != request.user:
        return redirect(comment_club.get_absolute_url())
    if request.method == "POST":
        form = OwnerCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()        
    form = OwnerCommentForm(instance=comment)
    context["form"] = form
    context["comment"] = comment
    return render_to_response(template_name, context)    
