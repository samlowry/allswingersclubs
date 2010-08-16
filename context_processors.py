from django.contrib.sites.models import Site
from keywords.models import Keyword
def get_current_site_id(request):
	""" returns current site object """
	current_site = Site.objects.get_current()
	return {'current_site': current_site}

def get_all_keywords(request):
    """ returns all keywords """
    return {"keywords": Keyword.on_site.all()} 
