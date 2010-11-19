from django.contrib.sites.models import Site
from keywords.models import Keyword
from keywords.models import KeywordState
from django.contrib.flatpages.models import FlatPage
from django.conf import settings

def get_current_site_id(request):
	""" returns current site object """
	current_site = Site.objects.get_current()
	return {'current_site': current_site}

def get_all_keywords(request):
    """ returns all keywords """
    if KeywordState.state.enabled():
        kw = Keyword.on_site.all()
    else:
        kw = None
    return {"keywords": kw} 

def get_current_site_flatpages(request):
	""" returns all flatpages of current site """
	flatpages = FlatPage.objects.filter(sites__id__exact=settings.SITE_ID).all()
	return {'flatpages': flatpages}
