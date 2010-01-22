from django.contrib import admin
from allswingersclubs.directory.models import *

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
	list_select_related = True

class StateAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'usps_name')
	list_display_links = ('id', 'name',)
	inlines = [CityInline,]

class ClubAdmin(admin.ModelAdmin):
	inlines = [PhotosInline,]
	list_display = ('id', 'name', 'city_name', 'state_name', 'description', 'is_closed', )
	list_display_links = ('id', 'name')
	list_editable = ('is_closed', )
	list_filter = ('is_closed', 'state',)
	list_per_page = 20
	ordering = ('state',)
	search_fields = ('id', 'name')
	actions_on_bottom = True
	
	def queryset(self, request):
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