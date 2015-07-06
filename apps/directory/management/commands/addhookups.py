import pprint

import random

import MySQLdb

import urllib
from urlparse import urlparse
from django.core.files import File

from django.core.management.base import BaseCommand, CommandError
from directory.models import *

class Command(BaseCommand):
    args = '<min_records_per_state max_records_per_state>'
    help = 'Add random number of hookup ads records to each state'



    def handle(self, *args, **options):
        
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="", # your password
                      db="prs",
                      cursorclass=MySQLdb.cursors.DictCursor
                      ) # name of the data base

        cur = db.cursor()

        all_states_list2 = State2.objects.all()

        for state in all_states_list2 :
            
            # number_of_records = random.randint(1,7)
            number_of_records = 1
            
            # cur.execute("SELECT * FROM header WHERE state='%s' LIMIT %s" % (state.name, number_of_records) )
            cur.execute("SELECT * FROM header WHERE state='%s' and CHAR_LENGTH(images) > 0 LIMIT %s" % (state.name, number_of_records) )
            rows = cur.fetchall()
            for row in rows :
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
                        title = row['header'].strip(),
                        description = row['body'].strip(),
                    )

                # parse attr data
                row['attr']=row['attr'].split(';')
                for attr in row['attr'] :
                    if len(attr) :
                        attr = attr.split(' : ')          
                        setattr(record,attr[0],attr[1].strip())

                pprint.pprint(record.__dict__,width=1)
                print "\n"

                record.save()

                # parse images data
                row['images']=row['images'].split(';')
                for image_url in row['images'] :
                    if len(image_url) :

                        photo = Photo2(
                                hookup=record,
                            )

                        name = urlparse(image_url).path.split('/')[-1]

                        print image_url;print "\n"

                        content = urllib.urlretrieve(image_url)

                        # See also: http://docs.djangoproject.com/en/dev/ref/files/file/
                        photo.original_image.save(name, File(open(content[0])), save=True)

                # 7) delete record in pool
                cur.execute("DELETE FROM header WHERE id='%s'" % row['id'] )


        

        # for poll_id in args:
        #     try:
        #         poll = Poll.objects.get(pk=int(poll_id))
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write('Successfully closed poll "%s"\n' % poll_id)