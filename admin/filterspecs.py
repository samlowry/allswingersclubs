from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site

class MultiSitesFilterSpec(FilterSpec):
	def __init__(self, f, request, params, model, model_admin):
		super(MultiSitesFilterSpec, self).__init__(f, request, params, model, model_admin)
		self.lookup_val = request.GET.get(f.name, None)
		self.lookup_choices = Site.objects.all()

	def title(self):
		return "sites"
		
	def choices(self, cl):
		yield {'selected': self.lookup_val is None,
				'query_string': cl.get_query_string({}, [self.field.name]),
				'display': _('All')}		

		for site in self.lookup_choices:
			yield {'selected': self.lookup_val == site,
					'query_string': cl.get_query_string({'sites__id': site.id}),
					'display': site}	
					
