# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns


urlpatterns = patterns(
    'forum.views',
    (r'^$', 'forum_index'),
    (r'^group/(?P<group_id>\d+)/$', 'forum_group'),
    (r'^topic/(?P<group_post_id>\d+)/$', 'forum_post'),
    (r'^user/(?P<user_id>\d+)/$', 'forum_user'),
)
