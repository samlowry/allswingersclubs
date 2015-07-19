import pprint

import random

import MySQLdb

import urllib
import requests

import HTMLParser

from urlparse import urlparse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.core.management.base import BaseCommand, CommandError
from directory.models import *

from django.contrib.sites.models import Site

def clean_string(self):
    self=self.strip()
    self=self.replace("\"'", "'")

    self=unicode(self, errors='ignore')

    h = HTMLParser.HTMLParser()
    self = h.unescape(self)
    
    return self

class Command(BaseCommand):
    args = '<min_records_per_state max_records_per_state>'
    help = 'Add random number of hookup ads records to each state'



    def handle(self, *args, **options):
        
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="prs", # your username
                      passwd="prs", # your password
                      db="prs",
                      cursorclass=MySQLdb.cursors.DictCursor
                      ) # name of the data base

        cur = db.cursor()

        all_states_list2 = State2.objects.all()

        for state in all_states_list2 :

            # if state.name != 'Texas': continue
            
            number_of_records = random.randint(1,10)
            # number_of_records = 1
            
            cur.execute("SELECT * FROM header WHERE state='%s' GROUP BY `town` ORDER BY rand() LIMIT %s" % (state.name, number_of_records) )
            # cur.execute("SELECT * FROM header WHERE state='%s' and CHAR_LENGTH(images) > 0 LIMIT %s" % (state.name, number_of_records) )
            rows = cur.fetchall()
            for row in rows :

                print "\n\n====================R=E=C=O=R=D====================\n\n"

                if len(row['body'])>0:

                    pprint.pprint(row)
                    print "\n"
                    
                    state = State2.objects.get(name=row['state'].strip())

                    try:
                        city = City.objects.get(name=row['town'].strip(),state=state)
                    except City.DoesNotExist:
                        print "!!!!!City.DoesNotExist!!!!\n"
                        city = City(name=row['town'].strip(),state=state)

                    record = Hookup(
                            city = city,
                            state = state,
                            title = clean_string(row['header']),
                            description = clean_string(row['body']),
                        )

                    # parse attr data
                    row['attr']=clean_string(row['attr'])
                    row['attr']=row['attr'].split(';')
                    for attr in row['attr'] :
                        if len(attr) :
                            attr = attr.split(' : ')
                            setattr(record,attr[0],attr[1])

                    pprint.pprint(record.__dict__,width=1)
                    print "\n"

                    record.save()
                    db.commit()
                    record.sites.add(Site.objects.get_current())
                    db.commit()

                    # parse images data
                    row['images']=row['images'].split(';')
                    for image_url in row['images'] :
                        if len(image_url) :

                            photo = Photo2(
                                    hookup=record,
                                )

                            name = urlparse(image_url).path.split('/')[-1]

                            print image_url;print "\n"

                            # content = urllib.urlretrieve(image_url)
                            try:
                                r = requests.get(image_url)

                                img_temp = NamedTemporaryFile(delete=True)
                                img_temp.write(r.content)
                                img_temp.flush()

                                # See also: http://docs.djangoproject.com/en/dev/ref/files/file/
                                # photo.original_image.save(name, File(open(content[0])), save=True)
                                photo.original_image.save(name, File(img_temp), save=True)
                            except:
                                pass
                                

                # 7) delete record in pool
                # print "DELETE FROM header WHERE id=%s \n" % row['id']
                cur.execute("DELETE FROM header WHERE id=%s" % row['id'] )
                db.commit()
