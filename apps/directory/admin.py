import copy

from django.contrib import admin
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ForeignKey
from django.db.models import options

from directory.models import *
from directory.forms import ClubAdminForm

def get_field(self, name, many_to_many=True):
	"""
	Returns the requested field by name. Raises FieldDoesNotExist on error.
	"""
	to_search = many_to_many and (self.fields + self.many_to_many) or self.fields
	if hasattr(self, '_copy_fields'):
		to_search += self._copy_fields
	for f in to_search:
		if f.name == name:
			return f
	if not name.startswith('__') and '__' in name:
		f = None 
		model = self 
		path = name.split('__') 
		for field_name in path: 
			f = model._get_field(field_name)
			if isinstance(f, ForeignKey):
				model = f.rel.to._meta
		f = copy.deepcopy(f)
		f.name = name
		if not hasattr(self, "_copy_fields"):
			self._copy_fields = list()
		self._copy_fields.append(f)
		return f
	raise FieldDoesNotExist, '%s has no field named %r' % (self.object_name, name)

setattr(options.Options, '_get_field', options.Options.get_field.im_func)
setattr(options.Options, 'get_field', get_field)

class PhotosInline(admin.TabularInline):
	model = Photo
	extra = 0
	max_num = 15

class ClubInline(admin.TabularInline):
	model = Club
	extra = 0
	max_num = 15

class CityInline(admin.TabularInline):
	model = City
	max_num = 15
	
	
class RegionAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


class CountryAdmin(admin.ModelAdmin):
	list_display = ('name', 'region', 'short_description', )
	search_fields = ('name', 'region__name')
	

class CityAdmin(admin.ModelAdmin):
	inlines = [ClubInline,]
	list_display = ('id', 'name', 'state_name', 'country_name')
	list_display_links = ('id', 'name')
	list_filter = ('state', 'country')
	search_fields = ('name',)
	list_select_related = True

class StateAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'usps_name', 'short_description', )
	list_display_links = ('id', 'name',)

class ClubAdmin(admin.ModelAdmin):
	inlines = [PhotosInline,]
	list_display = ('id', 'name', 'owner', 'city_name', 'state_name', 'country_name', 'short_description', 'is_closed', 'homepage_url', 'all_sites')
	list_display_links = ('id', 'name')
	list_editable = ('is_closed', )
	list_filter = ('sites', 'is_closed', 'state', 'city__country')
	list_per_page = 20
	ordering = ('state',)
	search_fields = ('id', 'name', 'city__name', 'city__country__name', 'email')
	actions_on_bottom = True
	form = ClubAdminForm
	fieldsets = [
				(None, {'fields': ['name', 'description', 'owner']}),
				(None, {'fields': ['address', 'country', 'state', 'city', 'phone', 
									'email', 'homepage', 'latitude', 'longitude']}),
				(None, {'fields': ['rating']}),
				(None, {'fields': ['date_of_review', 'is_closed']}),
				(None, {'fields': ['sites']}),
				]
	def queryset(self, request):
		q = request.GET.copy()
		
		# set filter for 'All' link. need to defferetiate All link click and empty request
		q["id__gt"] = 0
		
		# get state is from request
		state_id = int(request.GET.get("state__id__exact", 0))
		
		# get all states filter. if GET contains 'id__gt' then it was All link
		# if not, it was empty request
		all_states = request.GET.get("id__gt", None)

		if state_id:
			# get state id from session key
			session_state_id = int(request.session.get('state_id', 0))
			if session_state_id != state_id:
				# if they are not the same, replace session key with state id from request
				request.session["state_id"] = state_id
		else:
			# if there is no state
			if all_states == None:
				# if it's empty request update GET dict
				if request.session.has_key("state_id"):
					q["state__id__exact"] = request.session["state_id"]
		
		request.GET = q
		qs = super(ClubAdmin, self).queryset(request)
		return qs.select_related('state', 'city')
		
	
	
	
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'city':
			kwargs["queryset"] = City.objects.all().select_related('state')
			# return db_field.formfield(**kwargs)
		return super(ClubAdmin, self).formfield_for_foreignkey(db_field, request = request, **kwargs)
	

class PhotoAdmin(admin.ModelAdmin):
	list_display = ('id', 'club', 'original_image', 'admin_thumbnail_view')
	list_select_related = True
	search_fields = ('id', 'original_image')
	list_per_page = 10


admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Photo, PhotoAdmin)

admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
