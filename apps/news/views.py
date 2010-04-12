# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from news.forms import NewsForm
from directory.models import Club
from news.models import News

@login_required
def add(request, club_id, template_name="news/change_news_form.html"):
    """adds news"""
    context = RequestContext(request)
    cl = get_object_or_404(Club, id=club_id)
    if request.method == "POST":
        form = NewsForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = NewsForm()
    context["form"] = form
        
    return render_to_response(template_name, context)
    
@login_required
def change(request, news_id, template_name="news/change_news_form.html"):
    """changes news"""
    context = RequestContext(request)
    news = get_object_or_404(News, id=news_id)
    if request.method == "POST":
        form = NewsForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = NewsForm(instance=news)  
    context["form"] = form
    
    return render_to_response(template_name, context) 

    