# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PostAuthor'
        db.create_table('forum_postauthor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('forum', ['PostAuthor'])

        # Adding model 'GroupCategory'
        db.create_table('forum_groupcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('forum', ['GroupCategory'])

        # Adding model 'Group'
        db.create_table('forum_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('leader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.PostAuthor'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.GroupCategory'])),
        ))
        db.send_create_signal('forum', ['Group'])

        # Adding model 'GroupPost'
        db.create_table('forum_grouppost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Group'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.PostAuthor'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('forum', ['GroupPost'])

        # Adding model 'GroupPostComment'
        db.create_table('forum_grouppostcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.GroupPost'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.PostAuthor'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('forum', ['GroupPostComment'])

        # Adding model 'UserBlogPost'
        db.create_table('forum_userblogpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.PostAuthor'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('forum', ['UserBlogPost'])

        # Adding model 'UserBlogPostComment'
        db.create_table('forum_userblogpostcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog_post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.UserBlogPost'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.PostAuthor'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('forum', ['UserBlogPostComment'])


    def backwards(self, orm):
        # Deleting model 'PostAuthor'
        db.delete_table('forum_postauthor')

        # Deleting model 'GroupCategory'
        db.delete_table('forum_groupcategory')

        # Deleting model 'Group'
        db.delete_table('forum_group')

        # Deleting model 'GroupPost'
        db.delete_table('forum_grouppost')

        # Deleting model 'GroupPostComment'
        db.delete_table('forum_grouppostcomment')

        # Deleting model 'UserBlogPost'
        db.delete_table('forum_userblogpost')

        # Deleting model 'UserBlogPostComment'
        db.delete_table('forum_userblogpostcomment')


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