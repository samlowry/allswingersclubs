#-*- coding: utf8 -*-

import urllib, sys, re, os, time, codecs
from optparse import OptionParser

from django.core.validators import email_re # 1.1.1 version

#sys.setdefaultencoding('utf8')

parser = OptionParser()
parser.add_option("--club_id", dest="club_id", help=u"Process 1 club with specified ID", default='')
parser.add_option("--clubs_count", dest="clubs_count", help=u"Number of clubs to process", default='')
(options, args) = parser.parse_args()

if not options.club_id and not options.clubs_count:
    print 'Use -h to get list of available commands'
    sys.exit(1)

if options.club_id and options.clubs_count:
    print u'Use only one parameter - club_id OR clubs_count'
    sys.exit(1)
    

try:
    if options.club_id: options.club_id = int(options.club_id)
    if options.clubs_count: options.clubs_count = int(options.clubs_count)
except:
    print u'Incorrect parameter - must be an integer'
    sys.exit(1)
    
    
base = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
sys.path.insert(0, base(''))
sys.path.insert(1, base('apps'))

# set settings file
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from registration.models import *
from registration.views import _send_invitations

if options.club_id:
    club = Club.objects.get(pk=options.club_id)
    print 'processing club with email', club.email
    if not email_re.match(club.email):
        print 'invalid club email', club.email
        sys.exit(1)          
    # send invitation only if it just has been created
    inv, is_created = Invitation.objects.get_or_create(email=club.email)
    if is_created:                
        inv.email = club.email
        inv.save()
        inv.send()
        
if options.clubs_count:
    total_clubs_processed = 0   
    for club in Club.objects.all():
        if total_clubs_processed >= options.clubs_count: sys.exit()
        print 'processing club with email', club.email
        if email_re.match(club.email):       
            # send invitation only if it just has been created
            inv, is_created = Invitation.objects.get_or_create(email=club.email)
            if is_created:
                inv.email = club.email
                inv.save()
                inv.send()
                
                total_clubs_processed += 1
