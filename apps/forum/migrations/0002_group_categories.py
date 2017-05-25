# -*- coding: utf-8 -*-
import os.path
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        fixture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture_group_cateogy.json')
        call_command('loaddata', fixture_path)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'forum.group': {
            'Meta': {'object_name': 'Group'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.GroupCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'forum.groupcategory': {
            'Meta': {'object_name': 'GroupCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.grouppost': {
            'Meta': {'object_name': 'GroupPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'forum.grouppostcomment': {
            'Meta': {'object_name': 'GroupPostComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'group_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.GroupPost']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'forum.postauthor': {
            'Meta': {'object_name': 'PostAuthor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.userblogpost': {
            'Meta': {'object_name': 'UserBlogPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'forum.userblogpostcomment': {
            'Meta': {'object_name': 'UserBlogPostComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'blog_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.UserBlogPost']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['forum']
    symmetrical = True
