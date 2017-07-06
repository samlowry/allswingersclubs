# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.contrib.sites.models import get_current_site

from forum.models import Group, GroupPost, PostAuthor


def forum_index(request):
    groups = Group.current_site_only.all()
    return render(request, 'forum/index.html', {'groups': groups})


def forum_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id, site__id=get_current_site(request).id)
    posts = group.posts
    return render(request, 'forum/board.html', {'group': group, 'posts': posts})


def forum_post(request, group_post_id):
    post = get_object_or_404(GroupPost, pk=group_post_id)
    comments = post.comments

    return render(request, 'forum/topic.html', {
        'post': post,
        'comments': comments
    })


def forum_user(request, user_id):
    user = get_object_or_404(PostAuthor, pk=user_id)

    return render(request, 'forum/user_profile.html', {'user': user})
