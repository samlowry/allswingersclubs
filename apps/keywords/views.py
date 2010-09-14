# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.http import urlencode

from directory.models import Club
from reversion.models import ClubReversion
from keywords.forms import SearchForm

PER_PAGE = 20 # paginator's per page

def search(request, template_name="keywords/search.html"):
    """
        full text search with pagination
    """
    context = RequestContext(request)
    data = {} # data to the render
    params = dict(request.GET.items())
    # remove page num from params
    p = {}
    for k in params.keys():
        if k == "page":
            continue
        p[k] = params[k]
    search_text = request.GET.get("q")
    if search_text:
        clubs = Club.full_text.search(search_text)
        form = SearchForm(p)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        paginator = Paginator(clubs, PER_PAGE)
        try:
            clubs = paginator.page(page)
        except (EmptyPage, InvalidPage):
            clubs = paginator.page(paginator.num_pages)

        data["clubs"] = clubs
    else:
        form = SearchForm()
    data["query_string"] = "?%s" % urlencode(p)
    data["search_text"] = search_text
    data["form"] = form
    return render_to_response(template_name, data, context_instance=context)
