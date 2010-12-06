#-*- coding: utf-8 -*-
import sys, os
import urllib2


os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from settings import *
from directory.models import *


CLUBS = Club.objects.all()
for club in CLUBS:
    if club.homepage:
        try:
            urllib2.urlopen(club.homepage)
        except Exception, error:
            club.homepage = ''
            club.save()
            print "%s (%s) has error %s" % (club.id, club.homepage, error)
