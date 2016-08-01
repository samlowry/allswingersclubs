import pprint
import socket

import random
import urllib2

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

good_proxy = []
bad_proxy = []

curr_proxy_index = 0

def clean_string(self):
    self=self.strip()
    self=self.replace("\"'", "'")

    self=unicode(self, errors='ignore')

    h = HTMLParser.HTMLParser()
    self = h.unescape(self)
    
    return self

def verifyProxy( all_good = False ):
    global is_verify_proxylist
    result = ""
    listhandle = open( "proxylist.txt" ).read( ).split( '\n' )

    for line in listhandle:
        (phost, pport) = line.split( ":" )
        #print("host: %s, port: %s" % (phost, pport))

        if all_good == False:
            try:
                proxy_handler = urllib2.ProxyHandler( {'http': "http://%s/" % line} )
                opener = urllib2.build_opener( proxy_handler )
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib2.install_opener( opener )
                req = urllib2.Request( "http://www.google.com" )
                sock = urllib2.urlopen( req, timeout=120 )
                rs = sock.read( 1000 )
                if '<title>Google</title>' in rs:
                    good_proxy.append( line )
                    print( ('0', line) )
                else:
                    raise "Not Google"
            except:
                bad_proxy.append( line )
                print( ('x', line) )
        else:
            good_proxy.append( line )
    is_verify_proxylist = True

def getProxy():
    global curr_proxy_index
    result = ""
    if len( good_proxy ) > 0:
        result = good_proxy[curr_proxy_index]
        curr_proxy_index += 1
        if curr_proxy_index >= len(good_proxy):
            curr_proxy_index = 0
    return result

def write_to_log( log_f, msg = "" ):
    print( msg )
    log_f.write( msg + "\n" )

def add_hookups(*args):
    help = '<site_id table_name min_records_per_state max_records_per_state>'
    site_id=int(args[0])
    table_name=args[1]
    min_records_per_state=int(args[2])
    max_records_per_state=int(args[3])

    log_f = open( "/var/log/log_addhookups.txt", "w+" )

    # verifyProxy(True)
    # proxy_host = getProxy()
    # if proxy_host == "":
    #     write_to_log( log_f, "no find work proxy! script has been stoping!" )
    #     return

    # write_to_log( log_f, "proxy: %s" % proxy_host )

    write_to_log( log_f, "legend: LR - leave record, # - record number(id), CE - city error, AE - parse attributes error, IE - image error" )

    try:
        db = MySQLdb.connect(
            host="localhost", # your host, usually localhost
            user="addhookups", # your username
            passwd="addhookups",
            db="addhookups",
            cursorclass=MySQLdb.cursors.DictCursor
        ) # name of the data base
    except MySQLdb.Error:
        print( MySQLdb.Error )
    finally:
        cur = db.cursor()

        all_states_list2 = State2.objects.all()

        for state in all_states_list2 :

            number_of_records = random.randint(min_records_per_state,max_records_per_state)

            sql = "SELECT * FROM %s WHERE state='%s' GROUP BY `town` ORDER BY rand() LIMIT %s" % (table_name, state.name, number_of_records)
            write_to_log( log_f, sql )
            cur.execute(sql)
            # cur.execute("SELECT * FROM header WHERE state='%s' and CHAR_LENGTH(images) > 0 LIMIT %s" % (state.name, number_of_records) )
            rows = cur.fetchall()
            for row in rows :

                if len(row['body'])>0:

                    row_id = row['id']
                    city_error = "pass"
                    images = []
                    attributes_error = "pass"

                    state = State2.objects.get(name=row['state'].strip())

                    try:
                        city = City.objects.filter(name=row['town'].strip(),state=state)[0]
                    except City.DoesNotExist:
                        city_error = "!!!!!City.DoesNotExist!!!!"
                        city = City(name=row['town'].strip(),state=state)
                    except IndexError:
                        city_error = "!!!!!City IndexError!!!!"
                        city = City(name=row['town'].strip(),state=state)
                    except django.db.utils.DatabaseError, e:
                        city_error = "!!!!!Database error: %s!!!!" % e

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
                        if len(attr):
                            attr = attr.split(' : ')
                            if len( attr ) >= 3:
                                setattr(record,attr[0],attr[1])
                            else:
                                attributes_error = "cannot parse: %s -> %s" % ( row['attr'], attr )

                    #pprint.pprint(record.__dict__,width=1)

                    record.save()
                    db.commit()
                    record.sites.add(Site.objects.get(pk=site_id))
                    db.commit()

                    # parse images data
                    if row['images'] is not None:
                        row['images']=row['images'].split(';')
                        image_counter = 1
                        for image_url in row['images'] :
                            if len(image_url) :

                                photo = Photo2(
                                        hookup=record,
                                    )

                                name = urlparse(image_url).path.split('/')[-1]

                                # content = urllib.urlretrieve(image_url)
                                try:

                                    #r = requests.get(image_url)

                                    # proxy_handler = urllib2.ProxyHandler( {'http': "http://%s/" % proxy_host} )
                                    # opener = urllib2.build_opener( proxy_handler )
                                    
                                    opener = urllib2.build_opener( {'http': "http://%s/" % proxy_host} )

                                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                                    urllib2.install_opener( opener )


                                    f = urllib2.urlopen( image_url, timeout=120 )

                                    data = f.read()
                                    img_temp = NamedTemporaryFile(delete=True)
                                    img_temp.write(data)
                                    img_temp.flush()

                                    images.append( (image_counter, image_url, "ok") )

                                    # See also: http://docs.djangoproject.com/en/dev/ref/files/file/
                                    # photo.original_image.save(name, File(open(content[0])), save=True)
                                    photo.original_image.save(name, File(img_temp), save=True)
                                except urllib2.URLError, e:
                                    if hasattr( e, 'reason' ):
                                        if hasattr( e, 'code' ):
                                            images.append( (image_counter, image_url, e.code, e.reason) )
                                        else:
                                            images.append( (image_counter, image_url, e.reason) )
                                    elif hasattr( e, 'code' ):
                                        images.append( (image_counter, image_url, e.code) )
                                    else:
                                        images.append( (image_counter, image_url, e) )
                                    proxy_host = getProxy()
                                    write_to_log( log_f, "change proxy: %s" % proxy_host )
                                except socket.error, e:
                                    images.append( (image_counter, image_url, ("socket",e)) )
                                    proxy_host = getProxy( )
                                    write_to_log( log_f, "change proxy: %s" % proxy_host )



                # 7) delete record in pool
                # print "DELETE FROM header WHERE id=%s \n" % row['id']
                if attributes_error != "pass" or city_error != "pass":
                    write_to_log( log_f, "!LR #%d CE:%s, AE:%s, IE:%s" % (row_id, city_error, attributes_error, images) )
                else:
                    cur.execute("DELETE FROM header WHERE id=%s" % row['id'] )
                    db.commit()
                    write_to_log( log_f, "#%d CE:%s, AE:%s, IE:%s" % (row_id,city_error,attributes_error,images) )
    log_f.close()




class Command(BaseCommand):
    args = '<min_records_per_state max_records_per_state>'
    help = 'Add random number of hookup ads records to each state'



    def handle(self, *args, **options):
        add_hookups(1,'header',20,60);
        add_hookups(2,'fetish_header',5,20);
        
        
