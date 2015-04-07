# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TwitterConnection.consumer_key'
        db.add_column(u'services_social_twitterconnection', 'consumer_key',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'TwitterConnection.consumer_secret'
        db.add_column(u'services_social_twitterconnection', 'consumer_secret',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TwitterConnection.consumer_key'
        db.delete_column(u'services_social_twitterconnection', 'consumer_key')

        # Deleting field 'TwitterConnection.consumer_secret'
        db.delete_column(u'services_social_twitterconnection', 'consumer_secret')


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
            'consumer_key': ('django.db.models.fields.TextField', [], {}),
            'consumer_secret': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'services_social.youtubeconnection': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'YoutubeConnection'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['services_social']