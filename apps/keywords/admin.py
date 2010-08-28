from django.contrib import admin

from django.contrib.sites.models import Site
from keywords.forms import SiteAdminForm


class SiteAdmin(admin.ModelAdmin):
    form = SiteAdminForm

admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)


