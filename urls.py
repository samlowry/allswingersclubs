from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, Sitemap
from directory.models import State, State2, Country, City, Club, Hookup
from forum.models import Group, GroupPost
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


class State2Sitemap(Sitemap):
    changefreq = "always"
    priority = 0.8

    def items(self):
        return State2.objects.all()


class CountrySitemap(Sitemap):
    changefreq = "always"
    priority = 0.7

    def items(self):
        return Country.objects.all()


class CitySitemap(Sitemap):
    changefreq = "always"
    priority = 0.6

    def items(self):
        return City.objects.all()


class ClubSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Club.current_site_only.all()

    def lastmod(self, obj):
        return obj.date_of_review


class HookupSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Hookup.current_site_only.all()

    def lastmod(self, obj):
        return obj.date_of_publish


class ForumIndexSitemap(Sitemap):
    changefreq = "always"
    priority = 1
    location = '/forum/'

    def items(self):
        return ('',)

# class GroupSitemap(Sitemap):
#     changefreq = "daily"
#     priority = 0.5

#     def items(self):
#         return Group.current_site_only.all()


# class GroupPostSitemap(Sitemap):
#     changefreq = "daily"
#     priority = 0.5

#     def items(self):
#         return GroupPost.current_site_only.all()

#     def lastmod(self, obj):
#         return obj.created_at


sitemaps = {
    'index': IndexSitemap,
    'forumindex': ForumIndexSitemap,
    # 'forumboard': GroupSitemap,
    # 'forumpost': GroupPostSitemap,
    'state': StateSitemap,
    'state2': State2Sitemap,
    'country': CountrySitemap,
    'city': CitySitemap,
    'clubs': ClubSitemap,
    'hookups': HookupSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^news/', include('news.urls')),
    (r'^rss/', include('rss.urls')),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^comments/post/$', 'comments.views.post_wrapper'),   # must be before django comments urls
    (r'^comments/list/$', 'comments.views.comments_list'),
    (r'^comments/change/(?P<comment_id>\d+)/$', 'comments.views.comment_change'),
    (r'^comments/', include('django.contrib.comments.urls')),

    # Main app urls
    (r'^', include('directory.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^reversions/', include('reversion.urls')),
    (r'^tag/', include('tagging.urls')),
    (r'^search/', include('keywords.urls')),
    (r'^forum/', include('forum.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^(?P<path>.+\.(?:css|js|jpg|gif|png))$',
                            'django.views.static.serve', {'document_root': 'static'}) )
