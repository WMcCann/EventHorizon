# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterProfile'
        db.create_table(u'social_twitterprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('twitter_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('followers_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('friends_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('listed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('favourites_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('statuses_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'social', ['TwitterProfile'])

        # Adding model 'BrandTwitterProfile'
        db.create_table(u'social_brandtwitterprofile', (
            (u'twitterprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.TwitterProfile'], unique=True, primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Brand'])),
            ('first_load', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'social', ['BrandTwitterProfile'])

        # Adding model 'AdvertiserTwitterProfile'
        db.create_table(u'social_advertisertwitterprofile', (
            (u'twitterprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.TwitterProfile'], unique=True, primary_key=True)),
            ('advertiser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Advertiser'])),
            ('first_load', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'social', ['AdvertiserTwitterProfile'])

        # Adding model 'CampaignTwitterProfile'
        db.create_table(u'social_campaigntwitterprofile', (
            (u'twitterprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.TwitterProfile'], unique=True, primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Campaign'])),
            ('first_load', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'social', ['CampaignTwitterProfile'])


    def backwards(self, orm):
        # Deleting model 'TwitterProfile'
        db.delete_table(u'social_twitterprofile')

        # Deleting model 'BrandTwitterProfile'
        db.delete_table(u'social_brandtwitterprofile')

        # Deleting model 'AdvertiserTwitterProfile'
        db.delete_table(u'social_advertisertwitterprofile')

        # Deleting model 'CampaignTwitterProfile'
        db.delete_table(u'social_campaigntwitterprofile')


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
        u'core.campaign': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Campaign'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brand']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ending_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_sap': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'initiation_date': ('django.db.models.fields.DateTimeField', [], {}),
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
        u'core.person': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Person'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
        u'social.advertiserfacebookpage': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'AdvertiserFacebookPage', '_ormbases': [u'social.FacebookPage']},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Advertiser']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'facebookpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.FacebookPage']", 'unique': 'True', 'primary_key': 'True'}),
            'first_load': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'social.advertisertwitterprofile': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'AdvertiserTwitterProfile', '_ormbases': [u'social.TwitterProfile']},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Advertiser']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'twitterprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.TwitterProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'social.brandfacebookpage': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'BrandFacebookPage', '_ormbases': [u'social.FacebookPage']},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brand']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'facebookpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.FacebookPage']", 'unique': 'True', 'primary_key': 'True'}),
            'first_load': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'social.brandtwitterprofile': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'BrandTwitterProfile', '_ormbases': [u'social.TwitterProfile']},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brand']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'twitterprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.TwitterProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'social.campaignfacebookpage': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'CampaignFacebookPage', '_ormbases': [u'social.FacebookPage']},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Campaign']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'facebookpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.FacebookPage']", 'unique': 'True', 'primary_key': 'True'}),
            'first_load': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'social.campaigntwitterprofile': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'CampaignTwitterProfile', '_ormbases': [u'social.TwitterProfile']},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Campaign']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'twitterprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.TwitterProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'social.facebookpage': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'FacebookPage'},
            'facebook_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'talking_about': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'social.facebookuser': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'FacebookUser'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Person']", 'unique': 'True'}),
            'picture': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'social.insightsfacebookpage': {
            'Meta': {'ordering': "[u'facebook_page']", 'object_name': 'InsightsFacebookPage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookPage']"}),
            'first_load_daily': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load_days_28': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load_dimensions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_load_weekly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'social.twitterprofile': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'TwitterProfile'},
            'favourites_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'friends_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'statuses_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['social']