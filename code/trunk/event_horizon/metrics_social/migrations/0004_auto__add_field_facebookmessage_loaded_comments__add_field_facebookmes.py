#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FacebookMessage.loaded_comments'
        db.add_column(u'metrics_social_facebookmessage', 'loaded_comments',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'FacebookMessage.loaded_likes'
        db.add_column(u'metrics_social_facebookmessage', 'loaded_likes',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FacebookMessage.loaded_comments'
        db.delete_column(u'metrics_social_facebookmessage', 'loaded_comments')

        # Deleting field 'FacebookMessage.loaded_likes'
        db.delete_column(u'metrics_social_facebookmessage', 'loaded_likes')


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
        u'metrics_social.facebookcomment': {
            'Meta': {'ordering': "[u'-created_time']", 'object_name': 'FacebookComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookUser']", 'null': 'True', 'blank': 'True'}),
            'author_facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_social.FacebookMessage']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_likes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'metrics_social.facebookinsightspagedaily': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'FacebookInsightsPageDaily'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'day': ('django.db.models.fields.DateField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.InsightsFacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_engaged_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_fan_adds': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_fan_removes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_fans': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_organic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_organic_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_viral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_viral_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_negative_feedback': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_negative_feedback_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_organic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_organic_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_viral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_viral_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_stories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_storytellers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_views_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'metrics_social.facebookinsightspagedays28': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'FacebookInsightsPageDays28'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.InsightsFacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'page_engaged_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_organic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_organic_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_viral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_viral_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_negative_feedback': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_negative_feedback_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_organic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_organic_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_viral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_viral_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_stories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_storytellers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'metrics_social.facebookinsightspageweekly': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'FacebookInsightsPageWeekly'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.InsightsFacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_engaged_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_organic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_organic_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_viral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_impressions_viral_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_negative_feedback': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_negative_feedback_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_organic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_organic_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_viral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_posts_impressions_viral_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_stories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page_storytellers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'week': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'metrics_social.facebookinsightspost': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'FacebookInsightsPost'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'day': ('django.db.models.fields.DateField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_social.FacebookMessage']"}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.InsightsFacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_consumptions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_consumptions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_engaged_users': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_fan': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_fan_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_fan_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_fan_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_organic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_organic_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_paid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_paid_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_viral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_impressions_viral_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_negative_feedback': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_negative_feedback_unique': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_stories': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_storytellers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "[u'-created_time']", 'object_name': 'FacebookMessage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookUser']", 'null': 'True', 'blank': 'True'}),
            'author_facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'comments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'facebook_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'loaded_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loaded_likes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'first_load': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['metrics_social']