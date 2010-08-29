from django.dispatch import dispatcher
from django.db.models.signals import post_syncdb
from django.contrib.sites.models import Site
from keywords import models as kw

def create_keywords(**kwargs):
    """creates initial keywords"""
    if kw.Keyword.objects.all().count() == 0:
        # create keywords
        site1 = Site.objects.get(id=1) # swingers
        sw1 = kw.Keyword(text="all swingers clubs")
        sw1.save(site1)

        sw2 = kw.Keyword(text="swingers us clubs")
        sw2.save(site1)

        sw3 = kw.Keyword(text="swingers france")
        sw3.save(site1)
        
        site2 = Site.objects.get(id=2)
        fet1 = kw.Keyword(text="all fetish clubs")
        fet1.save(site2)

        fet2 = kw.Keyword(text="texas club fetish")
        fet2.save(site2)

        fet3 = kw.Keyword(text="fetish clubs in paris")
        fet3.save(site2)

        site3 = Site.objects.get(id=3)
        gays1 = kw.Keyword(text="all gays clubs")
        gays1.save(site3)

        gays2 = kw.Keyword(text="gays usa club")
        gays2.save(site3)
        
        gays3 = kw.Keyword(text="gay club orlando")
        gays3.save(site3)
        print "New keywords created."
post_syncdb.connect(create_keywords, sender=kw)
