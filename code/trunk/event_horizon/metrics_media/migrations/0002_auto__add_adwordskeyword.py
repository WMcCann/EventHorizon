# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdwordsKeyword'
        db.create_table(u'metrics_media_adwordskeyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('adwords_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.AdwordsAccount'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('keyword_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('keyword_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('campaign_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('campaign_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('campaign', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('adgroup_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('adgroup_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('adgroup', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('placement_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('max_cpc', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('clicks', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('impressions', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('cost', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('search_impressions_share', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('search_exact_match', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('avg_position', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('week', self.gf('django.db.models.fields.DateField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_media', ['AdwordsKeyword'])


    def backwards(self, orm):
        # Deleting model 'AdwordsKeyword'
        db.delete_table(u'metrics_media_adwordskeyword')


    models = {
        u'core.advertiser': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Advertiser'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'company_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Company']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_sap': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.brand': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Brand'},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Advertiser']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Category']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Country']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_sap': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.category': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Sector']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.company': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Company'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Country']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_sap': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.country': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Country'},
            'cod_sap': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.sector': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Sector'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mnemonic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'media.adwordsaccount': {
            'Meta': {'ordering': "[u'adwords_connection']", 'object_name': 'AdwordsAccount'},
            'adwords_connection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services_media.AdwordsConnection']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brand']"}),
            'client_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load_ad': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load_keyword': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'metrics_media.adwordskeyword': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'AdwordsKeyword'},
            'adgroup': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adgroup_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adgroup_status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adwords_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.AdwordsAccount']"}),
            'avg_position': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'campaign': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'campaign_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'campaign_status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'clicks': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'cost': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'day': ('django.db.models.fields.DateField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'keyword_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'keyword_status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'max_cpc': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'placement_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'search_exact_match': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'search_impressions_share': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'week': ('django.db.models.fields.DateField', [], {})
        },
        u'services_media.adwordsconnection': {
            'Meta': {'ordering': "[u'email']", 'object_name': 'AdwordsConnection'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'credential': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['metrics_media']