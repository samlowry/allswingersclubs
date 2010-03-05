from django.contrib import admin
from directory.models import *

class PhotosInline(admin.TabularInline):
	model = Photo
	extra = 5
	max_num = 15

class ClubInline(admin.TabularInline):
	model = Club
	extra = 5
	max_num = 15

class CityInline(admin.TabularInline):
	model = City
	max_num = 15

class CityAdmin(admin.ModelAdmin):
	inlines = [ClubInline,]
	list_display = ('id', 'name', 'state_name')
	list_display_links = ('id', 'name')
	list_filter = ('state',)
	search_fields = ('name',)
	list_select_related = True

class StateAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'usps_name')
	list_display_links = ('id', 'name',)
	inlines = [CityInline,]

class ClubAdmin(admin.ModelAdmin):
	inlines = [PhotosInline,]
	list_display = ('id', 'name', 'city_name', 'state_name', 'description', 'is_closed', 'homepage_url', 'all_sites')
	list_display_links = ('id', 'name')
	list_editable = ('is_closed', )
	list_filter = ('sites', 'is_closed', 'state',)
	list_per_page = 20
	ordering = ('state',)
	search_fields = ('id', 'name',)
	actions_on_bottom = True
	
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