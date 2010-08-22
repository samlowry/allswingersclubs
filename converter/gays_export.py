# usage:
#    manage.py shell
#    from converter import gays_export
#    gays_export.main()

import csv
import re
from django.contrib.sites.models import Site
from directory.models import Club, State, City, Country, Region
from django.db.models import Q
from tagging.models import Tag

from django.core import management
from django.db.models import get_app

pat = re.compile(r"[0-9-]\d+")

def main():
    prepare()
    export()
    print "\nDone. See gays_export.log for details."
    
def prepare():
    """ creates countries with regions that are missed """
    countries = (
        ("China", "6"),
        ("Suriname", "4"),
        ("Malaysia", "6"),
        ("Finland", "1"),
        ("Singapore", "6"),
        ("Canada", "5"),
        ("Mexico", "5"),
        ("Philippines", "6"),
    )
    for co in countries:
        country, created = Country.objects.get_or_create(name=co[0], region=Region.objects.get(id=co[1]))
    
def export():
    # empty log file
    with open("converter/gays_export.log", "w") as f:
        pass 
    reader = csv.reader(open("converter/both_clubs.csv"), quoting=csv.QUOTE_ALL, delimiter="|")
    for row in reader:
        
        try:
            number, name, address, land, phone, descr, tags, url = row
            if not int(number) % 10:
                print "#",
            
            cl, created = Club.objects.get_or_create(name=name, address=address, phone=phone, description=descr, homepage=url)            

            city, state = land.split(",")
            if int(number) == 0:
                import pdb; pdb.set_trace()
            try:
                state_obj = get_state(state, number)
                
                cl.state = state_obj
                # try to get city with full coincidence (name and state)
                cities = City.objects.filter(name__iexact=city.strip(), state=state_obj)
                if city.strip() == "Washington":
                    cities = City.objects.filter(name__iexact="Washington")
                if cities.count() == 0:
                    # try to get with trail 'city'
                    cities = City.objects.filter(name__iexact="%s city" % city.strip(), state=state_obj)
                if cities.count() == 0:
                    # try to get with startswith
                    cities = City.objects.filter(name__startswith=city.strip(), state=state_obj)
                    
                if cities.count() == 0:
                    # try to find without state, but state must to be not null
                    cities = City.objects.filter(name__iexact=city.strip(), state__isnull=False)
                    
                if cities.count() == 0:
                    # try to find without state with trail city
                    cities = City.objects.filter(name__iexact="%s city" % city.strip(), state__isnull=False)
                
                if cities.count() == 0:
                    # try to find without state but name of the city startswith...
                    cities = City.objects.filter(name__startswith=city.strip(), state__isnull=False)
                    
                        
                if cities.count() > 1:
                    to_log("More then 1 city returned for city %s. csv line number %s. Used object with 0 index. it is %s with id %s" % (city, number, cities[0], cities[0].id))                
                if cities.count() == 0:
                    raise City.DoesNotExist
                # everithing ok, save city    
                cl.city = cities[0]
            except State.DoesNotExist:
                # find city without any state. need to check state absense, because city maybe with state (in US), and without state (in the world)
                # ex: Paris in the US, Paris in the Europe
                try:
                    cities = City.objects.filter(name__iexact=city.strip(), state__isnull=True)
                    if cities.count() == 0:
                        raise City.DoesNotExist
                    if cities.count() > 1:
                        to_log("More then 1 without state or country city returned for number %s (city: %s). Used object with 0 index." % (number, city))
                    cl.city = cities[0]
                except City.DoesNotExist:
                    # create city without state or country
                    new_city = City()
                    new_city.name = city
                    country_obj = get_country(state)
                    if country_obj:
                        new_city.country = country_obj
                        to_log("World city (%s) created in the country %s, number %s" % (city, state, number))
                    else:
                        # unknown country
                        to_log("World city (%s) created without any country. Country is (%s), number is (%s)" % (city, state, number))
                    new_city.save()
                    cl.city = new_city
                    
            except City.DoesNotExist:
                # state exists but city not. create it and write to log
                new_city = City()
                new_city.name = city
                new_city.state = state_obj
                new_city.save()
                cl.city = new_city
                to_log("US city (%s) with existing state (%s) created. Number %s" % (city, state, number))
            
            cl.save() # because of m2m
            cl.sites.add(Site.objects.get(domain__iexact="allgayclubs.org"))
            cl.save()
            
            # tags add
            for tag in tags.split(","):
                tag = tag.strip().replace(" ", "-")
                if len(tag) > 0:
                    Tag.objects.add_tag(cl, tag.strip().replace(" ", "-"), sites=[Site.objects.get(domain__iexact="allgayclubs.org")])
                
        except Exception, exc:
            to_log("Exception: %s.\n\n %s \n\n" % (str(exc), row))
                
def get_cities(city):
    """return list with cities. if not found, the list will be empty"""

    return cities

def get_country(country):
    country = pat.sub("", country).strip()
    countries = Country.objects.filter(name__iexact=country)
    if countries.count() == 0:
        to_log("Create %s country by hand" % country)
        with open("converter/creating_countries.txt", "a") as f:
            f.write('("%s", "")\n' % country)
        return False
    if countries.count() > 1:
        to_log("Returned more than one country for %s. used with 0 index." % country)
    return countries[0]
    
def get_state(state, number):
    state = state.strip()
    states = State.objects.filter(name__iexact=state.strip())
    if states.count() == 0:
        states = State.objects.filter(name__startswith=state.strip())

    if state == "DC":
        states = State.objects.filter(name__iexact="Washington, DC")
        
    if states.count() == 0:
        # split state and try again
        state = pat.sub("", state).strip()
        
        states = State.objects.filter(name__iexact=state.strip())
        
    
    if states.count() == 0:
        raise State.DoesNotExist

    if states.count() > 1:
        to_log("more then 1 states returned for %s with number %s. used 0 index" % (state, number))
    
    return states[0]
            
def to_log(message):
    with open("converter/gays_export.log", "a") as f:
        f.write(message)
        f.write("\n")
        