from django.contrib import admin

from tapes.models import ClubCapture

class ClubCaptureAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "created", "user", "club_admin_url",)
    ordering = ("-created",)
admin.site.register(ClubCapture, ClubCaptureAdmin)