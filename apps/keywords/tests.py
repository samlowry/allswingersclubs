"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.test import TestCase
from django.contrib.sites.models import Site
from django.test.client import Client
from django.http import HttpRequest
from keywords.models import Keyword 
from keywords.middleware import KeywordMiddleware

class KeywordTest(TestCase):
    def setUp(self):
        self.settings_MAX_STACK_LENGTH = 10
    def test_save_clean(self):
        """ tests saving and cleaning (removing from stack) """
        kw = Keyword()
        kw.text = "google search"
        kw.save()
        self.assertEquals(Keyword.objects.all().count(), 1)
        
        self.assertTrue(Site.objects.get_current() in kw.sites.all())
        for i in range(1, 40):
            # sleep just a little bit
            kw = Keyword()
            kw.text = "keyword %i" % i
            kw.save()
        # keywords objects length is not more then the max value
        self.assertEquals(Keyword.objects.all().count(), self.settings_MAX_STACK_LENGTH)

        # keywords from 3-d decade must remains
        self.assertEquals(Keyword.objects.filter(text__icontains="3").count(), self.settings_MAX_STACK_LENGTH)
        

class KeywordMiddlewareTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
    
    def send_request(self, url):
        mdl = KeywordMiddleware()
        self.request.META["HTTP_REFERER"] = url
        mdl.process_request(self.request)

    def test_google(self):
        real_url = "http://www.google.ru/search?hl=ru&source=hp&q=what+is+google&aq=f&aqi=g10&aql=&oq=&gs_rfai="         
        self.send_request(real_url)
        # checking the keywords stack
        self.assertEquals(Keyword.objects.filter(text__icontains="what is google").count(), 1) 

    def test_yahoo(self):
        real_url = "http://search.yahoo.com/search;_ylt=Ai_2Ut67WeLxIU9Gx88YI8ObvZx4?p=what+is+yahoo&toggle=1&cop=mss&ei=UTF-8&fr=yfp-t-701"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is yahoo").count(), 1)

#    def test_msn(self):
#        real_url = "http://www.bing.com/search?q=what+is+msn&x=0&y=0&form=MSNH14&qs=n"
#        self.send_request(real_url)
#        self.assertEquals(Keyword.objects.filter(text__icontains="what is msn").count(), 1)

    def test_bing(self):
        real_url = "http://www.bing.com/search?q=what+is+bing&go=&form=QBRE&filt=all"   
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is bing").count(), 1)

##    def test_live(self):
#        # real_url = ""
#        # self.send_request(real_url)
#        # self.assertEquals(Keyword.objects.filter(text__icontains="what is live").count(), 1)
#
    def test_aol(self):
        real_url = "http://search.aol.com/aol/search?s_it=comsearch40t&q=what+is+aol"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is aol").count(), 1)

    def test_ask(self):
        real_url = "http://www.ask.com/web?q=what+is+ask&search=&qsrc=0&o=0&l=dir"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is ask").count(), 1)

    def test_altavista(self):
        real_url = "http://www.altavista.com/web/results?fr=altavista&itag=ody&q=what+is+altavista&kgs=0&kls=0"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is altavista").count(), 1)

    #def test_feedster(self):
    #    real_url = ""
    #    self.send_request(real_url)
    #    self.assertEquals(Keyword.objects.filter(text__icontains="what is fidster").count(), 1)

    def test_lycos(self):
        real_url = "http://search.lycos.com/?tab=web&query=what+is+lycos&x=0&y=0&diktfc=CA53455CD397D61D988238E9D66CA4CCD20AED0637D1"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is lycos").count(), 1)

    def test_alltheweb(self):
        real_url = "http://www.alltheweb.com/search?cat=web&cs=iso88591&q=what+is+alltheweb&rys=0&itag=crv&_sb_lang=pref"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is alltheweb").count(), 1)

    def test_yandex(self):
        real_url = "http://yandex.ru/yandsearch?text=what+is+yandex&lr=2"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is yandex").count(), 1)

    def test_rambler(self):
        real_url = "http://nova.rambler.ru/search?btnG=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8!&query=what+is+rambler"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is rambler").count(), 1)

    def test_gogo(self):
        real_url = "http://gogo.ru/go?q=what%20is%20gogo&"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is gogo").count(), 1)

    def test_mail(self):
        real_url = "http://go.mail.ru/search?mailru=1&mg=1&q=what+is+mail"
        self.send_request(real_url)
        self.assertEquals(Keyword.objects.filter(text__icontains="what is mail").count(), 1)
