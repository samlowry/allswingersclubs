# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import get_current_site

from forum.models import Group, GroupPost, PostAuthor


def _paginate(request, query):
    paginator = Paginator(query, 2)
    page = request.GET.get('p', '1')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items


def forum_index(request):
    groups = _paginate(request, Group.objects.filter(site__id=get_current_site(request).id))
    return render_to_response('forum/index.html', {'groups': groups})


def forum_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id, site__id=get_current_site(request).id)
    posts = _paginate(request, group.grouppost_set.all())
    return render_to_response('forum/board.html', {'group': group, 'posts': posts})


def forum_post(request, group_post_id):
    post = get_object_or_404(GroupPost, pk=group_post_id)
    comments = _paginate(request, post.grouppostcomment_set.all())

    return render_to_response('forum/topic.html', {
        'post': post,
        'comments': comments
    })


def forum_user(request, user_id):
    user = get_object_or_404(PostAuthor, pk=user_id)

    return render_to_response('forum/user_profile.html', {'user': user})
