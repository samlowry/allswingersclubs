# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from directory.models import Club
from reversion.models import ClubReversion
from keywords.forms import SearchForm

def search(request, template_name="keywords/search.html"):
    context = RequestContext(request)
    clubs = None
    if request.method == "GET":
        search_text = request.GET.get("q")
        if search_text:
            clubs = Club.objects.search(search_text)
            form = SearchForm(request.GET)
        else:
            form = SearchForm()
    else:
        form = SearchForm()
    ctx = {}
    ctx["clubs"] = clubs
    ctx["form"] = form
    return render_to_response(template_name, ctx, context_instance=context)
