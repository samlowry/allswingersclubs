from django.contrib import admin
from allswingersclubs.linkator.models import *

class TradelinkInline(admin.TabularInline):
	model = Tradelink
	extra = 10

class TradelinkAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', '__unicode__', 'page')
	list_select_related = True

class PageAdmin(admin.ModelAdmin):
	inlines = [
		TradelinkInline,
	]

admin.site.register(Tradelink, TradelinkAdmin)
admin.site.register(Page, PageAdmin)