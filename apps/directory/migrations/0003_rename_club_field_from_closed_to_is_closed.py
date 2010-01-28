
from south.db import db
from django.db import models
from allswingersclubs.directory.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Renaming field 'Club.closed' to 'Club.is_closed'
        db.rename_column('directory_club', 'closed', 'is_closed')
    
    def backwards(self, orm):
        
        # Renaming field 'Club.is_closed' to 'Club.closed'
        db.rename_column('directory_club', 'is_closed', 'closed')
        
    
    
    models = {
        'directory.city': {
            'Meta': {'unique_together': "(('state', 'name'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['directory.State']"})
        },
        'directory.club': {
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['directory.City']", 'null': 'True', 'blank': 'True'}),
            'date_of_review': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['directory.State']"})
        },
        'directory.photo': {
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['directory.Club']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'directory.state': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'usps_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        }
    }
    
    complete_apps = ['directory']
