#-*- coding: utf8 -*-

import urllib, sys, re, os, time, codecs
from optparse import OptionParser

#sys.setdefaultencoding('utf8')
    
    
base = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
sys.path.insert(0, base(''))
sys.path.insert(1, base('apps'))

# set settings file
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from django.core.validators import email_re # >= 1.1.1 version
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from directory.models import *

csv_lines = open('swingers_clubs_WO_USA.csv', 'r').readlines()

for cl in csv_lines:
    if len(cl.split('\t')) < 8: continue
    
    location = strip_tags(cl.split('\t')[0]).replace('"', '')
    club_name = strip_tags(cl.split('\t')[1]).replace('"', '')
    address = strip_tags(cl.split('\t')[2]).replace('"', '')
    phone = strip_tags(cl.split('\t')[3]).replace('"', '')
    website = strip_tags(cl.split('\t')[4]).replace('"', '')
    description = strip_tags(cl.split('\t')[7]).replace('"', '')
    
    # clean
    if not website.startswith('http://'): website = ''
    
    # region & country
    if len(location.split('/')) < 2: continue
    
    region = location.split('/')[0]
    country = location.split('/')[1]
    
    if 'Australia' in region:
        db_region = Region.objects.get(name__istartswith='Australia')
    else:
        db_region = Region.objects.get(name__istartswith=region)
        
    # create country if needed
    db_country, is_created = Country.objects.get_or_create(region=db_region, name=country)
    
    if ',' in address:
        city = address.split(',')[0].strip()
    else:
        city = address.strip()
    
    db_city, is_created = City.objects.get_or_create(name=city, country=db_country)
    
    exists = True
    try:
        db_club = Club.objects.get(name=club_name.strip(), description=description.strip(), address=address.strip(), city=db_city, phone=phone.strip(), homepage=website.strip())
    except Club.DoesNotExist:
        exists = False
    except Exception, e:
        print e
        print cl, 'not saved'
        continue
        
    print club_name, exists
        
    if not exists:
        db_club = Club(name=club_name.strip(), description=description.strip(), address=address.strip(), city=db_city, phone=phone.strip(), homepage=website.strip()).save()
        #if not db_club: continue
        print db_club, 'created'
        db_club.sites = [Site.objects.get_current(),]
        db_club.save()
        
    #db_club, is_created = Club.objects.get_or_create(name=club_name.strip(), description=description.strip(), address=address.strip(), city=db_city, phone=phone.strip(), homepage=website.strip())
    #if is_created:
    #    db_club.sites = [Site.objects.get_current(),]
    #    db_club.save()
    
    #print region, country
    #print db_region, country
    
    #print location, club_name, address, phone, website, description
