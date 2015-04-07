# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdwordsConnection'
        db.create_table(u'services_media_adwordsconnection', (
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, primary_key=True)),
            ('credential', self.gf('oauth2client.django_orm.CredentialsField')(null=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'services_media', ['AdwordsConnection'])


    def backwards(self, orm):
        # Deleting model 'AdwordsConnection'
        db.delete_table(u'services_media_adwordsconnection')


    models = {
        u'services_media.adwordsconnection': {
            'Meta': {'ordering': "[u'email']", 'object_name': 'AdwordsConnection'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'credential': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['services_media']