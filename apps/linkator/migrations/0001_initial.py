
from south.db import db
from django.db import models
from allswingersclubs.linkator.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('linkator_page', (
            ('id', orm['linkator.Page:id']),
            ('path', orm['linkator.Page:path']),
        ))
        db.send_create_signal('linkator', ['Page'])
        
        # Adding model 'Tradelink'
        db.create_table('linkator_tradelink', (
            ('id', orm['linkator.Tradelink:id']),
            ('url', orm['linkator.Tradelink:url']),
            ('title', orm['linkator.Tradelink:title']),
            ('description', orm['linkator.Tradelink:description']),
            ('page', orm['linkator.Tradelink:page']),
        ))
        db.send_create_signal('linkator', ['Tradelink'])
        
        # Creating unique_together for [url, page] on Tradelink.
        db.create_unique('linkator_tradelink', ['url', 'page_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [url, page] on Tradelink.
        db.delete_unique('linkator_tradelink', ['url', 'page_id'])
        
        # Deleting model 'Page'
        db.delete_table('linkator_page')
        
        # Deleting model 'Tradelink'
        db.delete_table('linkator_tradelink')
        
    
    
    models = {
        'linkator.page': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'linkator.tradelink': {
            'Meta': {'unique_together': "(('url', 'page'),)"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linkator.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['linkator']
