from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from directory.models import State

@login_required
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