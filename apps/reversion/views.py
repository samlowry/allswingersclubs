# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404

from directory.models import Club
from reversion.models import ClubReversion
from directory.views import change_club

@login_required
def list_revisions(request, club_id, template_name="reversion/list.html"):
    """shows list of club's revisions"""
    club = get_object_or_404(Club, id=club_id)
    if club.owner == request.user:    
        context = RequestContext(request)
        context["club"] = club
        revisions = club.clubreversion_set.all().order_by("-created")
        context["revisions"] = revisions
    else:
        raise Http404
    return render_to_response(template_name, context)        

@login_required    
def show_revision(request, revision_id, template_name="reversion/show.html"):
    """shows revision_id revision. owner can revert to this revision"""
    revision = get_object_or_404(ClubReversion, id=revision_id)
    if revision.club.owner == request.user:    
        context = RequestContext(request)
        context["revision"] = revision
    else:
        raise Http404

    return render_to_response(template_name, context) 
        
@login_required
def revert(request, revision_id):
    """reverts to revision_id(with saving), shows club change form"""
    revision = get_object_or_404(ClubReversion, id=revision_id)
    if revision.club.owner == request.user:
        # revert club to current revision
        revision.revert()
    else:
        raise Http404    
    # redirect to club's changing address
    return redirect(reverse(change_club, args=[revision.club.id]))
    
