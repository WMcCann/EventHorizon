# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterMessage'
        db.create_table(u'metrics_social_twittermessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.TwitterProfile'])),
            ('twitter_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author_twitter_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('favorites', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('retweets', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('replies', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('is_retweet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loaded_favorites', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loaded_retweets', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loaded_replies', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_social', ['TwitterMessage'])

        # Adding unique constraint on 'TwitterMessage', fields ['twitter_profile', 'twitter_id']
        db.create_unique(u'metrics_social_twittermessage', ['twitter_profile_id', 'twitter_id'])

        # Adding model 'TwitterRetweet'
        db.create_table(u'metrics_social_twitterretweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_social.TwitterMessage'])),
            ('author_twitter_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_social', ['TwitterRetweet'])

        # Adding unique constraint on 'TwitterRetweet', fields ['message', 'author_twitter_id']
        db.create_unique(u'metrics_social_twitterretweet', ['message_id', 'author_twitter_id'])

        # Adding model 'TwitterFavorite'
        db.create_table(u'metrics_social_twitterfavorite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_social.TwitterMessage'])),
            ('author_twitter_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_social', ['TwitterFavorite'])

        # Adding unique constraint on 'TwitterFavorite', fields ['message', 'author_twitter_id']
        db.create_unique(u'metrics_social_twitterfavorite', ['message_id', 'author_twitter_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TwitterFavorite', fields ['message', 'author_twitter_id']
        db.delete_unique(u'metrics_social_twitterfavorite', ['message_id', 'author_twitter_id'])

        # Removing unique constraint on 'TwitterRetweet', fields ['message', 'author_twitter_id']
        db.delete_unique(u'metrics_social_twitterretweet', ['message_id', 'author_twitter_id'])

        # Removing unique constraint on 'TwitterMessage', fields ['twitter_profile', 'twitter_id']
        db.delete_unique(u'metrics_social_twittermessage', ['twitter_profile_id', 'twitter_id'])

        # Deleting model 'TwitterMessage'
        db.delete_table(u'metrics_social_twittermessage')

        # Deleting model 'TwitterRetweet'
        db.delete_table(u'metrics_social_twitterretweet')

        # Deleting model 'TwitterFavorite'
        db.delete_table(u'metrics_social_twitterfavorite')


    models = {
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
        u'metrics_social.evolutionfacebookpagelike': {
            'Meta': {'ordering': "[u'facebook_page']", 'object_name': 'EvolutionFacebookPageLike'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'metrics_social.facebookcomment': {
            'Meta': {'ordering': "[u'-created_time']", 'unique_together': "((u'facebook_id', u'message'),)", 'object_name': 'FacebookComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookUser']", 'null': 'True', 'blank': 'True'}),
            'author_facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_social.FacebookMessage']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_likes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'metrics_social.facebooklike': {
            'Meta': {'ordering': "[u'-created_at']", 'unique_together': "((u'message', u'author_facebook_id'),)", 'object_name': 'FacebookLike'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookUser']", 'null': 'True', 'blank': 'True'}),
            'author_facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_social.FacebookMessage']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'metrics_social.facebookmessage': {
            'Meta': {'ordering': "[u'-created_time']", 'unique_together': "((u'facebook_page', u'facebook_id'),)", 'object_name': 'FacebookMessage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookUser']", 'null': 'True', 'blank': 'True'}),
            'author_facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'comments': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'loaded_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loaded_likes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shares': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'metrics_social.insightsmetric': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'InsightsMetric'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'day': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dimension': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_social.FacebookMessage']", 'null': 'True', 'blank': 'True'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.InsightsFacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'metrics_social.twitterfavorite': {
            'Meta': {'ordering': "[u'-created_at']", 'unique_together': "((u'message', u'author_twitter_id'),)", 'object_name': 'TwitterFavorite'},
            'author_twitter_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_social.TwitterMessage']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'metrics_social.twittermessage': {
            'Meta': {'ordering': "[u'-created_time']", 'unique_together': "((u'twitter_profile', u'twitter_id'),)", 'object_name': 'TwitterMessage'},
            'author_twitter_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'favorites': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_retweet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loaded_favorites': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loaded_replies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loaded_retweets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'replies': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'retweets': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.TwitterProfile']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'metrics_social.twitterretweet': {
            'Meta': {'ordering': "[u'-created_at']", 'unique_together': "((u'message', u'author_twitter_id'),)", 'object_name': 'TwitterRetweet'},
            'author_twitter_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_social.TwitterMessage']"}),
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

    complete_apps = ['metrics_social']