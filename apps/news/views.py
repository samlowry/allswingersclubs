# Create your views here.
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from news.forms import NewsForm
from directory.models import Club
from news.models import News

@login_required
def add(request, club_id, template_name="news/change_news_form.html"):
    """adds news"""
    context = RequestContext(request)
    club = get_object_or_404(Club, id=club_id)
    if club.owner == request.user:
        if request.method == "POST":
            form = NewsForm(data=request.POST)
            if form.is_valid():
                news_object = form.save(commit=False)
                news_object.club = club
                news_object.save()
                # redirect to change page

                return redirect(reverse(change, args=[news_object.id]))
        else:
            form = NewsForm()
        context["form"] = form
        context["club"] = club
    else:
        #print "forbidden. it's not your club"
        return redirect(club.get_absolute_url())
        
    return render_to_response(template_name, context)
    
@login_required
def change(request, news_id, template_name="news/change_news_form.html"):
    """changes news"""
    context = RequestContext(request)
    news = get_object_or_404(News, id=news_id)
    if news.club.owner == request.user:    
        if request.method == "POST":
            form = NewsForm(request.POST, instance=news)
            if form.is_valid():
                form.save()
        else:
            # it's not post, show current new for changing
            form = NewsForm(instance=news)  
        context["form"] = form
        context["news"] = news
    else:
        #print "forbidden. it's not your club"    
        return redirect(news.club.get_absolute_url())        
    
    return render_to_response(template_name, context) 

@login_required
def news_list(request, club_id, template_name="news/list_news.html"):
    """shows all news of the club"""
    club = get_object_or_404(Club, id=club_id)
    if club.owner == request.user:       
        context=RequestContext(request)
        # get club's news
        news = club.news_set.all().order_by("-changed")
        context["news"] = news
        context["club"] = club
        return render_to_response(template_name, context)
    else:
        #print "forbidden. it's not your club"
        return redirect(club.get_absolute_url())
    
@login_required
def delete_news(request, news_id):
    """deletes news"""
    news = get_object_or_404(News, id=news_id)
    if news.club.owner == request.user:
        news.delete()
        return redirect(reverse(news_list, args=[news.club.id]))
    else:
        #print "forbidden. it's not your club"
        return redirect(news.club.get_absolute_url())  

def show(request, news_id, template_name="news/show.html"):
    """shows news"""
    context = RequestContext(request)
    news = get_object_or_404(News, id=news_id)
    context["news"] = news
    return render_to_response(template_name, context)