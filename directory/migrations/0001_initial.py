
from south.db import db
from django.db import models
from allswingersclubs.directory.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Club'
        db.create_table('directory_club', (
            ('id', orm['directory.Club:id']),
            ('name', orm['directory.Club:name']),
            ('description', orm['directory.Club:description']),
            ('address', orm['directory.Club:address']),
            ('state', orm['directory.Club:state']),
            ('city', orm['directory.Club:city']),
            ('phone', orm['directory.Club:phone']),
            ('email', orm['directory.Club:email']),
            ('homepage', orm['directory.Club:homepage']),
            ('latitude', orm['directory.Club:latitude']),
            ('longitude', orm['directory.Club:longitude']),
            ('rating', orm['directory.Club:rating']),
            ('date_of_review', orm['directory.Club:date_of_review']),
        ))
        db.send_create_signal('directory', ['Club'])
        
        # Adding model 'Photo'
        db.create_table('directory_photo', (
            ('id', orm['directory.Photo:id']),
            ('original_image', orm['directory.Photo:original_image']),
            ('club', orm['directory.Photo:club']),
        ))
        db.send_create_signal('directory', ['Photo'])
        
        # Adding model 'City'
        db.create_table('directory_city', (
            ('id', orm['directory.City:id']),
            ('name', orm['directory.City:name']),
            ('state', orm['directory.City:state']),
        ))
        db.send_create_signal('directory', ['City'])
        
        # Adding model 'State'
        db.create_table('directory_state', (
            ('id', orm['directory.State:id']),
            ('name', orm['directory.State:name']),
            ('usps_name', orm['directory.State:usps_name']),
        ))
        db.send_create_signal('directory', ['State'])
        
        # Creating unique_together for [state, name] on City.
        db.create_unique('directory_city', ['state_id', 'name'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [state, name] on City.
        db.delete_unique('directory_city', ['state_id', 'name'])
        
        # Deleting model 'Club'
        db.delete_table('directory_club')
        
        # Deleting model 'Photo'
        db.delete_table('directory_photo')
        
        # Deleting model 'City'
        db.delete_table('directory_city')
        
        # Deleting model 'State'
        db.delete_table('directory_state')
        
    
    
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
