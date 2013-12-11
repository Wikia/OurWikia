# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TopWikiaUsers'
        db.create_table(u'app_topwikiausers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('wikia_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.WikiaUser'])),
            ('wiki', self.gf('django.db.models.fields.related.ForeignKey')(related_name='top_users', to=orm['app.Wiki'])),
        ))
        db.send_create_signal(u'app', ['TopWikiaUsers'])

        # Adding unique constraint on 'TopWikiaUsers', fields ['position', 'wikia_user', 'wiki']
        db.create_unique(u'app_topwikiausers', ['position', 'wikia_user_id', 'wiki_id'])

        # Adding field 'Wiki.headline'
        db.add_column(u'app_wiki', 'headline',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Wiki.edits'
        db.add_column(u'app_wiki', 'edits',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Wiki.articles'
        db.add_column(u'app_wiki', 'articles',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Wiki.pages'
        db.add_column(u'app_wiki', 'pages',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Wiki.users'
        db.add_column(u'app_wiki', 'users',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Wiki.active_users'
        db.add_column(u'app_wiki', 'active_users',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'TopWikiaUsers', fields ['position', 'wikia_user', 'wiki']
        db.delete_unique(u'app_topwikiausers', ['position', 'wikia_user_id', 'wiki_id'])

        # Deleting model 'TopWikiaUsers'
        db.delete_table(u'app_topwikiausers')

        # Deleting field 'Wiki.headline'
        db.delete_column(u'app_wiki', 'headline')

        # Deleting field 'Wiki.edits'
        db.delete_column(u'app_wiki', 'edits')

        # Deleting field 'Wiki.articles'
        db.delete_column(u'app_wiki', 'articles')

        # Deleting field 'Wiki.pages'
        db.delete_column(u'app_wiki', 'pages')

        # Deleting field 'Wiki.users'
        db.delete_column(u'app_wiki', 'users')

        # Deleting field 'Wiki.active_users'
        db.delete_column(u'app_wiki', 'active_users')


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
            'last_editor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edits'", 'null': 'True', 'to': u"orm['app.WikiaUser']"}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'total_downvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': u"orm['app.Wiki']"})
        },
        u'app.topwikiausers': {
            'Meta': {'unique_together': "(('position', 'wikia_user', 'wiki'),)", 'object_name': 'TopWikiaUsers'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'top_users'", 'to': u"orm['app.Wiki']"}),
            'wikia_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.WikiaUser']"})
        },
        u'app.upvote': {
            'Meta': {'object_name': 'UpVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upvotes'", 'to': u"orm['app.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upvotes'", 'to': u"orm['auth.User']"})
        },
        u'app.wiki': {
            'Meta': {'object_name': 'Wiki'},
            'active_users': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'articles': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'edits': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'subdomain': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True'}),
            'users': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
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