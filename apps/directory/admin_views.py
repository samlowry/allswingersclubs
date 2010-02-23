from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from directory.models import State
import urllib2 # need to send request to the google geocoder
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def state_cities(request, state_id):
    """ gets request and state id, returns list of state's cities in the json format

if response.status == 0 then exception occurs and response.error contains error string
if response.status == 1 then response contains list of cities(id, name)
                                        
    """
    
    cities_list = [{"id": x.id, "name": x.__unicode__()} for x in State.objects.get(id=state_id).city_set.all()]

    try:
        answer = {'status': 1,
                  'cities': cities_list}
        json_answer = simplejson.dumps(answer)
        return HttpResponse(json_answer, mimetype='application/json')

    except Exception, err:
        error = str(err)
        answer_error = {'status': 0, 'error': error}
        json_answer_error = simplejson.dumps(answer_error)    
        return HttpResponse(json_answer_error, mimetype='application/json')
        
@staff_member_required
def geocoder_proxy(request):
    """ passes data from request to the google geocoder, return latitude and longitude """
    KEY = "222222" # google map key
    address = request.GET.get("q", "")
    if len(address) > 0:
        address = address.replace(" ", "+")
        url = """
http://maps.google.com/maps/geo?
q=%s&
key=%s&
sensor=false&
output=json&
oe=utf-8
    """ % (address, KEY)
        url = url.replace("\n", "")
        
        try:
            f = urllib2.urlopen(url)
            resp = simplejson.loads(f.read())
            # success code is 200, otherwise raise an exception
            if int(resp["Status"]["code"]) != 200:
                raise Exception("Can't retrieve coordinates. Sorry.");
            # latitude in json representations - Placemark[0].Point.coordinates[1]
            latitude = resp["Placemark"][0]["Point"]["coordinates"][1]
            # longitude in json representations - Placemark[0].Point.coordinates[0]
            longitude = resp["Placemark"][0]["Point"]["coordinates"][0]
            answer = {'status': 1,
                      'latitude': latitude,
                      'longitude': longitude
                      }
            json_answer = simplejson.dumps(answer)
            return HttpResponse(json_answer, mimetype='application/json')

        except Exception, err:
            error = str(err)
            answer_error = {'status': 0, 'error': error}
            json_answer_error = simplejson.dumps(answer_error)    
            return HttpResponse(json_answer_error, mimetype='application/json')
    else:
        json_answer = simplejson.dumps(answer_error)    
        return HttpResponse(json_answer_error, mimetype='application/json')
