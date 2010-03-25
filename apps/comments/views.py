from django.contrib.comments.views.comments import post_comment
from django.views.decorators.http import require_POST

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
	return post_comment(request, next)
	