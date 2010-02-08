
from south.db import db
from django.db import models
from linkator.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Page.site'
        db.add_column('linkator_page', 'site', orm['linkator.page:site'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Page.site'
        db.delete_column('linkator_page', 'site_id')
        
    
    
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
