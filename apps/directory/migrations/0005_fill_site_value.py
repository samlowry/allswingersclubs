
from south.db import db
from django.db import models
from directory.models import *
from django.contrib.sites.models import *

class Migration:
    
    
    no_dry_run = True
    
    def forwards(self, orm):
        "Write your forwards migration here"
        s1 = Site.objects.get(id=1)
        for club in Club.objects.all():
            try:
                club.sites.add(s1)
            except ValueError:
                pass
            club.save()
    
    
    def backwards(self, orm):
        "Write your backwards migration here"
        s1 = Site.objects.get(id=1)
        for club in Club.objects.all():
            try:
                club.sites.remove(s1)
            except ValueError:
                pass
            club.save()    
    
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
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'to': "orm['sites.Site']"}),
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
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['directory']
