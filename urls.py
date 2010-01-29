from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, Sitemap
from directory.views import index
from directory.models import *
import settings

admin.autodiscover()

class IndexSitemap(Sitemap):
	changefreq = "always"
	priority = 1
	location = '/'
	
	def items(self):
	    return ('',)

class StateSitemap(Sitemap):
	changefreq = "always"
	priority = 0.8

	def items(self):
	    return State.objects.all()

class ClubSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
	    return Club.open_only.all()

	def lastmod(self, obj):
		return obj.date_of_review

sitemaps = {
    'index': IndexSitemap,
    'state': StateSitemap,
    'clubs': ClubSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	
	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

	#Main app urls
	(r'^', include('directory.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('', (r'^(?P<path>.+\.(?:css|js|jpg|gif|png))$', 'django.views.static.serve', {'document_root': 'static'}) )
