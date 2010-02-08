
from south.db import db
from django.db import models
from linkator.models import *
from django.contrib.sites.models import *

class Migration:
    
    def forwards(self, orm):
        "Write your forwards migration here"
        s1 = Site.objects.get(id=1)
        for page in Page.objects.all():
            try:
                page.site = s1
            except ValueError:
                pass
            page.save()
    
    
    def backwards(self, orm):
        "Write your backwards migration here"
        for page in Page.objects.all():
            try:
                page.site = ''
            except ValueError:
                pass
            page.save()    
    
    models = {
        'linkator.page': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'linkator.tradelink': {
            'Meta': {'unique_together': "(('url', 'page'),)"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linkator.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['linkator']
