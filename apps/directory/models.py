import datetime
import random
from imagekit.models import ImageModel

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings

from directory.templatetags.my_slugify import my_slugify

def rating_random():
    return random.choice([3.0, 3.5, 4.0])
    
# Create your models here.
class State(models.Model):
	name = models.CharField('state name', max_length=20, unique=True)
	usps_name = models.CharField('USPS 2 letters state codename', max_length=2, unique=True)
	
	def __unicode__(self):
		return '%s (%s)' % (self.name, self.usps_name)
		
	class Meta:
		ordering = ['name']

	@models.permalink
	def get_absolute_url(self):
		return ('directory.views.state', (), {
			'state_usps_name': str(self.usps_name.lower()),
		})


class City(models.Model):
	name = models.CharField('City name', max_length=50)
	state = models.ForeignKey(State)

	class Meta:
		verbose_name_plural = "cities"
		ordering = ['state','name']
		unique_together = ('state', 'name')

	def __unicode__(self):
		return '%s, %s' % (self.name, self.state.usps_name)
		
	def state_name(self):
		return self.state
	state_name.short_description = 'State'
	state_name.admin_order_field = 'state'

class OpenClubsFromCurrentSiteManager(models.Manager):
	def get_query_set(self):
		return super(OpenClubsFromCurrentSiteManager, self).get_query_set().filter(sites__id__exact=settings.SITE_ID, is_closed=False)

class Club(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(blank=True)
	address = models.CharField('Street address', max_length=100, blank=True)
	state = models.ForeignKey(State)
	city = models.ForeignKey(City, blank=True, null=True)
	phone = models.CharField(max_length=30, blank=True)
	email = models.EmailField('e-mail', blank=True)
	homepage = models.URLField(blank=True, verify_exists=False)
	latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
	RATING_CHOISES = (
		(0.5, 0.5),
		(1, 1),
		(1.5, 1.5),
		(2, 2),
		(2.5, 2.5),
		(3, 3),
		(3.5, 3.5),
		(4, 4),
		(4.5, 4.5),
		(5, 5),
	)
	rating = models.FloatField(choices=RATING_CHOISES, default=rating_random)
	date_of_review = models.DateField(default=datetime.date.today)
	is_closed = models.BooleanField( default=False )
	objects = models.Manager()
	current_site_only = CurrentSiteManager('sites')
	open_only = OpenClubsFromCurrentSiteManager()
	sites = models.ManyToManyField(Site)
	owner = models.ForeignKey(User, null=True, blank=True)
	
	class Meta:
		ordering = ['name']
		# ordering = ['id']
	
	def __unicode__(self):
		return self.name

	def state_name(self):
		return self.state
	state_name.short_description = 'State'
	state_name.admin_order_field = 'state'

	def city_name(self):
		return self.city.name
	city_name.short_description = 'City'
	city_name.admin_order_field = 'city'
	
	@models.permalink
	def get_absolute_url(self):
		return ('directory.views.club', (), {
			'club_id': int(self.id),
			'club_urlsafe_title': str(my_slugify(self.name)),
		})
	def homepage_url(self):
		""" returns html formatted homepage url """
		return "<a href='%(url)s'>%(url)s</a>" % {"url": self.homepage}
	homepage_url.allow_tags = True

	def all_sites(self):
		sites_ = ",".join([s.name for s in self.sites.all()]) 
		# another way is return site domain. just change s.name with s.domain
		return sites_
	all_sites.short_description = 'Published on'
	
	def save(self):
		"""checks the owner of club, if owner changed saves event to the ClubCapture table"""

		if self.id is not None:
			from tapes.models import ClubCapture
			if Club.objects.get(id=self.id).owner != self.owner:
				capture = ClubCapture()
				capture.user = self.owner
				capture.club = self
				capture.save()
		super(Club, self).save()
			

class Photo(ImageModel):
	original_image = models.ImageField(upload_to='photos')
	club = models.ForeignKey(Club)

	class IKOptions:
		# This inner class is where we define the ImageKit options for the model
		spec_module = 'directory.specs'
		cache_dir = 'resized'
		image_field = 'original_image'
