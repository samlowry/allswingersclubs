from django.contrib.sites.models import Site

def get_current_site_id(request):
	""" returns current site object """
	current_site = Site.objects.get_current()
	return {'current_site': current_site}
 
