from django.shortcuts import render_to_response
from django.http import HttpResponsePermanentRedirect
from directory.templatetags.my_slugify import my_slugify
from django.core.urlresolvers import reverse
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext
from django.conf import settings
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

from comments.forms import get_comment_form
from directory.models import *
from news.models import News
from directory.forms import PhotoForm, ClubForm

from decorators import *

from django.forms.models import inlineformset_factory
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect


def index(request):
    all_states_list = State.objects.all()
    flatpages = FlatPage.objects.filter(sites__id__exact=settings.SITE_ID).all()
    
    news = News.objects.filter(club__sites__id__exact=settings.SITE_ID).order_by('-created')[:10]
    
    regions = Region.objects.all()
    
    return render_to_response(
        'directory/index.html',
        {
            'all_states_list': all_states_list,
            'flatpages': flatpages,
            'news': news,
            'regions': regions,
        },
        context_instance=RequestContext(request),
    )

@render_to('directory/category_region.html')    
def state(request, state_usps_name):
    region = State.objects.filter(usps_name__exact=state_usps_name).get()
    region.kind = 'state'
    clubs = Club.open_only.select_related('state','city').filter(state__usps_name__exact=state_usps_name).order_by('name')
    cities_w_clubs = City.objects.filter(state__usps_name__exact=state_usps_name).filter(club__id__in=clubs).values('id')
    empty_cities = City.objects.filter(state__usps_name__exact=state_usps_name).exclude(id__in = cities_w_clubs)    
    regions = State.objects.all()
    news = News.objects.filter(club__sites__id__exact=settings.SITE_ID).filter(club__state__id__exact=region.id).order_by('-created')[:10]

    return locals()



@render_to('directory/category_region.html')
def country(request, slug):
    region = get_object_or_404(Country, slug=slug)
    region.kind = 'country'
    clubs = Club.open_only.select_related('country','city').filter(city__country=region)
    regions = Country.objects.all()
    news = News.objects.filter(club__sites__id__exact=settings.SITE_ID).filter(club__city__country=region).order_by('-created')[:10]
    
    return locals()
    

@csrf_protect
def club(request, club_id, club_urlsafe_title):
    try:
        current_club = Club.current_site_only.select_related('state','city').filter(id__exact=club_id).get()
    except Club.DoesNotExist:
        raise Http404
    real_club_urlsafe_title=my_slugify(current_club.name)
    # # here we do 301 redirect if club is closed
    # if(current_club.is_closed):
    #     return HttpResponsePermanentRedirect(
    #         current_club.state.get_absolute_url()
    #     )
    if(club_urlsafe_title != real_club_urlsafe_title):
        return HttpResponsePermanentRedirect(
            current_club.get_absolute_url()
        )
    else:
        current_club.photos = current_club.photo_set.all()
        if current_club.state:
            all_clubs_for_state = Club.open_only.filter(state__usps_name__exact=current_club.state.usps_name).exclude(pk=current_club.pk)
        else:
            all_clubs_for_state = None
            
        try:
            if current_club.city.country:
                all_clubs_for_country = Club.open_only.select_related('state','city').filter(city__country=current_club.city.country).exclude(pk=current_club.pk)
            else:
                all_clubs_for_country = None
        except AttributeError:
            all_clubs_for_country = None

        news = current_club.news_set.all()
        
        form = get_comment_form(request, target_object=current_club)     
        return render_to_response(
            'directory/club.html',
            {
                'club': current_club,
                'all_clubs_for_state': all_clubs_for_state,
                'all_clubs_for_country': all_clubs_for_country,
                'form': form,
                'news': news,
            },
            context_instance=RequestContext(request),
        )

@login_required
@render_to('directory/tradingmap.html')
def tradingmap(request):
    if not request.user.is_superuser:
        raise Http404
    all_countries = Country.objects.all()
    all_states = State.objects.all()
    all_flatpages = FlatPage.objects.filter(sites__id__exact=settings.SITE_ID).all()
    all_clubs = Club.current_site_only.all()
    return locals()

@login_required    
def change_club(request, club_id, template_name="change_club.html"):
    context = RequestContext(request)
    # find club by id
    cl = Club.objects.get(id=club_id)
    
    # if it's not club's owner redirect to club page
    if request.user != cl.owner:
        return redirect(cl.get_absolute_url())

    PhotoFormSet = inlineformset_factory(Club, Photo, form=PhotoForm, max_num=7, extra=1, can_delete=False)

    if request.method == "POST":
        form = ClubForm(data=request.POST, instance=cl)
        formset = PhotoFormSet(request.POST, request.FILES, instance=cl)
        if form.is_valid() and formset.is_valid():
            # this action need to save to revision.
            changed_club = form.save(commit=False)
            changed_club.save(create_revision=True)
            formset.save()
            return redirect(reverse(change_club, args=[cl.id]))
    else:
        form = ClubForm(instance=cl)
        formset = PhotoFormSet(instance=cl)

    context["formset"] = formset
    context["form"] = form
    context["club"] = cl
        
    return render_to_response(template_name, context_instance=context)

@login_required
def clubs(request, template_name='clubs_list.html'):
    """all clubs of the user"""
    context = RequestContext(request)
    # get user's clubs
    all_clubs = Club.objects.filter(owner=request.user)
    context["clubs"] = all_clubs
    return render_to_response(template_name, context_instance=context)

def take_club(request, club_id):
    """sets registered user as club owner"""
    if request.user.is_anonymous():
        # offer to register or login
        return redirect('/accounts/anonymous/')
    else:
        club = get_object_or_404(Club, id=club_id)
        if club.owner is not None:
            # club has owner
            raise Http404
        club.owner = request.user
        club.email = request.user.email
        club.save(create_revision=True)
        context = RequestContext(request)
        context["club"] = club
        return redirect(reverse(change_club, args=[club.id]))

    
@login_required      
def add_club(request, template_name="change_club.html"):
    """ adds new club to the database """
    context = RequestContext(request)
    PhotoFormSet = inlineformset_factory(Club, Photo, extra=1, max_num=7, can_delete=False)

    empty_club = Club()
    if request.method == "POST":
                     
        form = ClubForm(data=request.POST)
        formset = PhotoFormSet(request.POST, request.FILES)
            
        if form.is_valid():
            club_object = form.save(commit=False)
            club_object.owner = request.user
            club_object.save() # Club instance need to have primary key before m2m relationship can be used
            club_object.sites = [Site.objects.get_current(),]
            club_object.save()
            # saving formset with images
            formset = PhotoFormSet(request.POST, request.FILES, instance=club_object)

            if formset.is_valid():
                
                formset.save()
            return redirect(reverse(club_added, args=[club_object.id]))            
    else:
        
        formset = PhotoFormSet(instance=empty_club)
        
        form = ClubForm()
        

    context["form"] = form
    context["formset"] = formset
    context["add_club"] = True
    
    return render_to_response(template_name, context)    
    
    
@login_required      
def club_added(request, club_id, template_name="club_added.html"):
    """ inform user about successful club adding """
    context = RequestContext(request)
    # find club by id
    cl = Club.objects.get(id=club_id)
    
    # if it's not club's owner redirect to club page
    if request.user != cl.owner:
        return redirect(cl.get_absolute_url())
        
    site = Site.objects.get_current()
    context["club"] = cl
    context["site"] = site
        
    return render_to_response(template_name, context_instance=context)

@render_to('directory/ajax_city_countries_options.html')
def ajax_get_country_cities(request):
    if not request.is_ajax(): raise Http404
    country = get_object_or_404(Country, pk=request.POST.get('country_id',0))
    cities_options = country.country_cities.all()
    return locals()
