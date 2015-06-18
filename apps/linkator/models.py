from django.db import models
from django.contrib.sites.models import Site

# Create your models here.
class Page(models.Model):
	path = models.CharField(max_length=100)
	site = models.ForeignKey(Site)
	
	class Meta:
		ordering = ['id']
		unique_together = (("site", "path"),)
		
	
	def __unicode__(self):
		return '%s%s' % (self.site, self.path,)
	

class Tradelink(models.Model):
	url = models.URLField('Partner\'s link')
	title = models.CharField('Text of the link', max_length=100)
	description = models.CharField('Additional description', max_length=255, blank=True)
	page = models.ForeignKey(Page)
	
	class Meta:
		ordering = ['id']
		unique_together = ('url', 'page')
	
	def __unicode__(self):
		return '%s' % (self.url, )
	
