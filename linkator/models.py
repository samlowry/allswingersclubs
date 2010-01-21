from django.db import models

# Create your models here.
class Page(models.Model):
	path = models.CharField(max_length=100, unique=True)
	
	class Meta:
		ordering = ['id']
	
	def __unicode__(self):
		return '%s' % (self.path,)

class Tradelink(models.Model):
	url = models.URLField('Partner\'s link', verify_exists=False)
	title = models.CharField('Text of the link', max_length=100)
	description = models.CharField('Additional description', max_length=255, blank=True)
	page = models.ForeignKey(Page)
	
	class Meta:
		ordering = ['id']
		unique_together = ('url', 'page')
	
	def __unicode__(self):
		return '%s' % (self.url, )
		
