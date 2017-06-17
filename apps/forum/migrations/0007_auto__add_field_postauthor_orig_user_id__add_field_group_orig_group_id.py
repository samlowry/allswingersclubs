# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        return
        # Adding field 'Group.group_id'
        db.add_column('forum_group', 'orig_group_id',
                      self.gf('django.db.models.fields.IntegerField')(default=None),
                      keep_default=False)

        db.execute('UPDATE forum_group SET orig_group_id=id')
        db.create_index('forum_group', ['orig_group_id'], unique=False)

        # Adding field 'GroupPost.post_id'
        db.add_column('forum_grouppost', 'orig_post_id',
                      self.gf('django.db.models.fields.IntegerField')(default=None),
                      keep_default=False)
        db.execute('UPDATE forum_grouppost SET orig_post_id=id')
        db.create_index('forum_grouppost', ['orig_post_id'], unique=False)

        # Adding field 'PostAuthor.orig_user_id'
        db.add_column('forum_postauthor', 'orig_user_id',
                      self.gf('django.db.models.fields.IntegerField')(default=None),
                      keep_default=False)

        db.execute('UPDATE forum_postauthor SET orig_user_id=id')
        db.create_index('forum_postauthor', ['orig_user_id'], unique=False)

        db.execute('ALTER TABLE forum_group MODIFY description LONGTEXT');

        db.execute('ALTER TABLE forum_grouppost ADD group_id INT');
        db.create_index('forum_grouppost', ['group_id'])

    def backwards(self, orm):
        # Deleting field 'PostAuthor.orig_user_id'
        db.delete_column('forum_postauthor', 'orig_user_id')

        # Deleting field 'Group.orig_group_id'
        db.delete_column('forum_group', 'orig_group_id')


        # Changing field 'Group.description'
        db.alter_column('forum_group', 'description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))
        # Deleting field 'GroupPost.orig_post_id'
        db.delete_column('forum_grouppost', 'orig_post_id')


    models = {
        'forum.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'orig_group_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'forum.grouppost': {
            'Meta': {'object_name': 'GroupPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_post_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'orig_user_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'})
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
