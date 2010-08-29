# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'page', fields ['path']
        db.delete_unique('linkator_page', ['path'])

        # Adding unique constraint on 'Page', fields ['path', 'site']
        db.create_unique('linkator_page', ['path', 'site_id'])


    def backwards(self, orm):
        
        # Adding unique constraint on 'page', fields ['path']
        db.create_unique('linkator_page', ['path'])

        # Removing unique constraint on 'Page', fields ['path', 'site']
        db.delete_unique('linkator_page', ['path', 'site_id'])


    models = {
        'linkator.page': {
            'Meta': {'unique_together': "(('site', 'path'),)", 'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'linkator.tradelink': {
            'Meta': {'unique_together': "(('url', 'page'),)", 'object_name': 'Tradelink'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['linkator.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['linkator']
