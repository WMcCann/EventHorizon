# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'YoutubeConnection.id'
        db.delete_column(u'services_social_youtubeconnection', u'id')

        # Adding field 'YoutubeConnection.email'
        db.add_column(u'services_social_youtubeconnection', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, primary_key=True),
                      keep_default=False)

        # Adding field 'YoutubeConnection.credential'
        db.add_column(u'services_social_youtubeconnection', 'credential',
                      self.gf('oauth2client.django_orm.CredentialsField')(null=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'YoutubeConnection.id'
        raise RuntimeError("Cannot reverse this migration. 'YoutubeConnection.id' and its values cannot be restored.")
        # Deleting field 'YoutubeConnection.email'
        db.delete_column(u'services_social_youtubeconnection', 'email')

        # Deleting field 'YoutubeConnection.credential'
        db.delete_column(u'services_social_youtubeconnection', 'credential')


    models = {
        u'services_social.facebookconnection': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'FacebookConnection'},
            'access_token': ('django.db.models.fields.TextField', [], {}),
            'conn_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'services_social.twitterconnection': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'TwitterConnection'},
            'access_token': ('django.db.models.fields.TextField', [], {}),
            'access_token_secret': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'services_social.youtubeconnection': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'YoutubeConnection'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'credential': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['services_social']