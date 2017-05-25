# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.db import models


class PostAuthor(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)


class GroupCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)


class Group(models.Model):
    site = models.ForeignKey(Site, null=False, blank=False, on_delete=models.CASCADE)
    leader = models.ForeignKey(PostAuthor, null=False, blank=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(GroupCategory, blank=False, null=False)


class GroupPost(models.Model):
    group = models.ForeignKey(Group, null=False, blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(PostAuthor, null=False, blank=False)

    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField()


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


class UserBlogPostComment(models.Model):
    blog_post = models.ForeignKey(UserBlogPost, null=False, blank=False)
    author = models.ForeignKey(PostAuthor, null=False, blank=False)

    content = models.TextField()
    created_at = models.DateTimeField()
