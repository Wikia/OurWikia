# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Wiki'
        db.create_table(u'app_wiki', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wordmark', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True)),
            ('title', self.gf('django.db.models.fields.TextField')(null=True)),
            ('wam_score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True)),
            ('subdomain', self.gf('django.db.models.fields.TextField')(null=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Wiki'])

        # Adding model 'WikiaUser'
        db.create_table(u'app_wikiauser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('avatar', self.gf('django.db.models.fields.URLField')(max_length=1024)),
        ))
        db.send_create_signal(u'app', ['WikiaUser'])

        # Adding model 'Story'
        db.create_table(u'app_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article_id', self.gf('django.db.models.fields.IntegerField')()),
            ('wiki', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['app.Wiki'])),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True)),
            ('total_upvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_downvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_editor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='edits', to=orm['app.WikiaUser'])),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'app', ['Story'])

        # Adding unique constraint on 'Story', fields ['article_id', 'wiki']
        db.create_unique(u'app_story', ['article_id', 'wiki_id'])

        # Adding model 'UpVote'
        db.create_table(u'app_upvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='upvotes', to=orm['app.Story'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='upvotes', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'app', ['UpVote'])

        # Adding model 'DownVote'
        db.create_table(u'app_downvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='downvotes', to=orm['app.Story'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='downvotes', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'app', ['DownVote'])

        # Adding model 'Comment'
        db.create_table(u'app_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['auth.User'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['app.Comment'])),
        ))
        db.send_create_signal(u'app', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Story', fields ['article_id', 'wiki']
        db.delete_unique(u'app_story', ['article_id', 'wiki_id'])

        # Deleting model 'Wiki'
        db.delete_table(u'app_wiki')

        # Deleting model 'WikiaUser'
        db.delete_table(u'app_wikiauser')

        # Deleting model 'Story'
        db.delete_table(u'app_story')

        # Deleting model 'UpVote'
        db.delete_table(u'app_upvote')

        # Deleting model 'DownVote'
        db.delete_table(u'app_downvote')

        # Deleting model 'Comment'
        db.delete_table(u'app_comment')


    models = {
        u'app.comment': {
            'Meta': {'object_name': 'Comment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': u"orm['app.Comment']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['auth.User']"})
        },
        u'app.downvote': {
            'Meta': {'object_name': 'DownVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'downvotes'", 'to': u"orm['app.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'downvotes'", 'to': u"orm['auth.User']"})
        },
        u'app.story': {
            'Meta': {'unique_together': "(('article_id', 'wiki'),)", 'object_name': 'Story'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'article_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_editor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edits'", 'to': u"orm['app.WikiaUser']"}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'total_downvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': u"orm['app.Wiki']"})
        },
        u'app.upvote': {
            'Meta': {'object_name': 'UpVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upvotes'", 'to': u"orm['app.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upvotes'", 'to': u"orm['auth.User']"})
        },
        u'app.wiki': {
            'Meta': {'object_name': 'Wiki'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'wam_score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'wordmark': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'})
        },
        u'app.wikiauser': {
            'Meta': {'object_name': 'WikiaUser'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']