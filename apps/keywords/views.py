# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from directory.models import Club
from reversion.models import ClubReversion

def search(request, template_name="keywords/search.html"):
    context = RequestContext(request)
    clubs = Club.current_site_only.all()

    return render_to_response(template_name, {"clubs": clubs}, context_instance=context)
