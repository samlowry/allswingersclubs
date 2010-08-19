from django.dispatch import dispatcher
from django.db.models.signals import post_syncdb

from keywords import models as kw

def create_keywords(**kwargs):
    """creates initial keywords"""
    if kw.Keyword.objects.all().count() == 0:
        # create keywords
        sw1 = kw.Keyword(text="all swingers clubs")
        sw1.save()
        sw1.sites.add(1)

        sw2 = kw.Keyword(text="swingers us clubs")
        sw2.save()
        sw2.sites.add(1)

        sw3 = kw.Keyword(text="swingers france")
        sw3.save()
        sw3.sites.add(1)

        fet1 = kw.Keyword(text="all fetish clubs")
        fet1.save()
        fet1.sites.add(2)

        fet2 = kw.Keyword(text="texas club fetish")
        fet2.save()
        fet2.sites.add(2)

        fet3 = kw.Keyword(text="fetish clubs in paris")
        fet3.save()
        fet3.sites.add(2)

        gays1 = kw.Keyword(text="all gays clubs")
        gays1.save()
        gays1.sites.add(3)

        gays2 = kw.Keyword(text="gays usa club")
        gays2.save()
        gays2.sites.add(3)
        
        gays3 = kw.Keyword(text="gay club orlando")
        gays3.save()
        gays3.sites.add(3)
        print "New keywords created."
post_syncdb.connect(create_keywords, sender=kw)
