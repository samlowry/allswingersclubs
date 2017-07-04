# -*- coding: utf-8 -*-

from datetime import datetime
from django.contrib.sites.models import Site
from django.db import models
from django.contrib.sites.managers import CurrentSiteManager
import settings


class PostAuthor(models.Model):
    orig_user_id = models.IntegerField(blank=False, null=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, blank=False, null=False)


class Group(models.Model):
    site = models.ForeignKey(Site, null=False, blank=False, on_delete=models.CASCADE)
    orig_group_id = models.IntegerField(blank=False, null=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    current_site_only = CurrentSiteManager('site')

    @property
    def posts(self, all=False):
        now = datetime.now()
        query = self.grouppost_set

        if not all:
            query = query.filter(created_at__lte=now)

        return query.all()

    @models.permalink
    def get_absolute_url(self):
        return ('forum.views.forum_group', (), {
            'group_id': int(self.id),
        })

class GroupPostCurrentSiteManager(models.Manager):
    def get_query_set(self):
        return super(GroupPostCurrentSiteManager, self).get_query_set().filter(group__site=settings.SITE_ID)    

class GroupPost(models.Model):
    group = models.ForeignKey(Group, null=False, blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(PostAuthor, null=False, blank=False)

    orig_post_id = models.IntegerField(blank=False, null=False, unique=True, db_index=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField()
    current_site_only = GroupPostCurrentSiteManager()

    @property
    def comments(self, all=False):
        now = datetime.now()
        query = self.grouppostcomment_set

        if not all:
            query = query.filter(created_at__lte=now)

        return query.all()

    @models.permalink
    def get_absolute_url(self):
        return ('forum.views.forum_post', (), {
            'group_post_id': int(self.id),
        })


class GroupPostComment(models.Model):
    group_post = models.ForeignKey(GroupPost, null=False, blank=False)
    author = models.ForeignKey(PostAuthor, null=False, blank=False)

    content = models.TextField()
    created_at = models.DateTimeField()


class UserBlogPost(models.Model):
    author = models.ForeignKey(PostAuthor, null=False, blank=False)

    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField()

    @property
    def comments(self, all=False):
        now = datetime.now()
        query = self.userblogpostcomment_set

        if not all:
            query = query.filter(created_at__lte=now)

        return query.all()


class UserBlogPostComment(models.Model):
    blog_post = models.ForeignKey(UserBlogPost, null=False, blank=False)
    author = models.ForeignKey(PostAuthor, null=False, blank=False)

    content = models.TextField()
    created_at = models.DateTimeField()
