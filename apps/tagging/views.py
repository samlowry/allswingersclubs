"""
Tagging related views.
"""
from django.http import Http404
from django.utils.translation import ugettext as _
# from django.views.generic.list_detail import object_list
from django.views.generic.list import ListView

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from tagging.models import Tag, TaggedItem
from tagging.utils import get_tag, get_queryset_and_model
from directory.models import *


def tagged_object_list(request, queryset_or_model=None, tag=None,
        related_tags=False, related_tag_counts=True, **kwargs):
    """
    A thin wrapper around
    ``django.views.generic.list_detail.object_list`` which creates a
    ``QuerySet`` containing instances of the given queryset or model
    tagged with the given tag.

    In addition to the context variables set up by ``object_list``, a
    ``tag`` context variable will contain the ``Tag`` instance for the
    tag.

    If ``related_tags`` is ``True``, a ``related_tags`` context variable
    will contain tags related to the given tag for the given model.
    Additionally, if ``related_tag_counts`` is ``True``, each related
    tag will have a ``count`` attribute indicating the number of items
    which have it in addition to the given tag.
    """
    if queryset_or_model is None:
        try:
            queryset_or_model = kwargs.pop('queryset_or_model')
        except KeyError:
            raise AttributeError(_('tagged_object_list must be called with a queryset or a model.'))

    if tag is None:
        try:
            tag = kwargs.pop('tag')
        except KeyError:
            raise AttributeError(_('tagged_object_list must be called with a tag.'))

    tag_instance = get_tag(tag)
    if tag_instance is None:
        raise Http404(_('No Tag found matching "%s".') % tag)
    queryset = TaggedItem.objects.get_by_model(queryset_or_model, tag_instance)
    if not kwargs.has_key('extra_context'):
        kwargs['extra_context'] = {}
    kwargs['extra_context']['tag'] = tag_instance
    if related_tags:
        kwargs['extra_context']['related_tags'] = \
            Tag.objects.related_for_model(tag_instance, queryset_or_model,
                                          counts=related_tag_counts)
    return ListView.as_view(request, queryset, **kwargs)

    
def country_clubs(request, country_name, tag_name, template_name="tagging/region_clubs.html"):
    """ filters clubs by tag_name and and country, passes clubs, tag_name and region to the context """
    tag_instance = get_tag(tag_name)
    if tag_instance is None:
        raise Http404(_('No Tag found matching "%s".') % tag_name)
    country = get_object_or_404(Country, slug=country_name)
    clubs = Club.current_site_only.filter(city__country=country)
    tagged_clubs = TaggedItem.objects.get_by_model(clubs, tag_instance.name)
    if len(tagged_clubs) == 0:
	    raise Http404(_('No Tag found matching "%s".') % tag_name)        
    context = {}
    context["region"] = country
    context["clubs"] = tagged_clubs
    context["seeking_tag"] = tag_instance   
    return render_to_response(template_name, context, context_instance=RequestContext(request))
    
def state_clubs(request, usps, tag_name, template_name="tagging/region_clubs.html"):
    """ filters clubs by tag_name and usps, passes clubs, tag_name and region to the context """
    tag_instance = get_tag(tag_name)
    if tag_instance is None:
        raise Http404(_('No Tag found matching "%s".') % tag)
    state = get_object_or_404(State, usps_name=usps)
    clubs = Club.current_site_only.filter(state=state)
    tagged_clubs = TaggedItem.objects.get_by_model(clubs, tag_instance.name)
    if len(tagged_clubs) == 0:
	    raise Http404(_('No Tag found matching "%s".') % tag_name)    
    context = {}
    context["region"] = state
    context["clubs"] = tagged_clubs
    context["seeking_tag"] = tag_instance
    return render_to_response(template_name, context, context_instance=RequestContext(request))
