#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FacebookInsightsPageDaily'
        db.delete_table(u'metrics_social_facebookinsightspagedaily')

        # Deleting model 'FacebookInsightsPageWeekly'
        db.delete_table(u'metrics_social_facebookinsightspageweekly')

        # Deleting model 'FacebookInsightsPost'
        db.delete_table(u'metrics_social_facebookinsightspost')

        # Deleting model 'FacebookInsightsPageDays28'
        db.delete_table(u'metrics_social_facebookinsightspagedays28')

        # Adding model 'InsightsFacebookPageDays28'
        db.create_table(u'metrics_social_insightsfacebookpagedays28', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('page_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_social', ['InsightsFacebookPageDays28'])

        # Adding model 'InsightsFacebookPageDaily'
        db.create_table(u'metrics_social_insightsfacebookpagedaily', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('page_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_fans', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_fan_adds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_fan_removes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_views_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_social', ['InsightsFacebookPageDaily'])

        # Adding model 'InsightsFacebookPageWeekly'
        db.create_table(u'metrics_social_insightsfacebookpageweekly', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('page_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_social', ['InsightsFacebookPageWeekly'])

        # Adding model 'InsightsFacebookPost'
        db.create_table(u'metrics_social_insightsfacebookpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            ('facebook_message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_social.FacebookMessage'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('post_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_fan', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_fan_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_fan_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_fan_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_consumptions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_consumptions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'metrics_social', ['InsightsFacebookPost'])


    def backwards(self, orm):
        # Adding model 'FacebookInsightsPageDaily'
        db.create_table(u'metrics_social_facebookinsightspagedaily', (
            ('page_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page_posts_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('page_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('page_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('page_posts_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_views_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_posts_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_fan_removes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_fan_adds', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_fans', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'metrics_social', ['FacebookInsightsPageDaily'])

        # Adding model 'FacebookInsightsPageWeekly'
        db.create_table(u'metrics_social_facebookinsightspageweekly', (
            ('page_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('page_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_posts_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page_posts_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('page_posts_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'metrics_social', ['FacebookInsightsPageWeekly'])

        # Adding model 'FacebookInsightsPost'
        db.create_table(u'metrics_social_facebookinsightspost', (
            ('post_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_consumptions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('post_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_consumptions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_social.FacebookMessage'])),
            ('post_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_fan_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('post_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_fan_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('post_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('post_impressions_fan_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_impressions_fan', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'metrics_social', ['FacebookInsightsPost'])

        # Adding model 'FacebookInsightsPageDays28'
        db.create_table(u'metrics_social_facebookinsightspagedays28', (
            ('page_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, auto_now_add=True, blank=True)),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('page_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('facebook_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.InsightsFacebookPage'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_posts_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_negative_feedback', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_stories', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page_posts_impressions_organic', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_organic_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_storytellers', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_engaged_users', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('page_posts_impressions_viral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_posts_impressions_paid_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions_viral_unique', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('page_impressions', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'metrics_social', ['FacebookInsightsPageDays28'])

        # Deleting model 'InsightsFacebookPageDays28'
        db.delete_table(u'metrics_social_insightsfacebookpagedays28')

        # Deleting model 'InsightsFacebookPageDaily'
        db.delete_table(u'metrics_social_insightsfacebookpagedaily')

        # Deleting model 'InsightsFacebookPageWeekly'
        db.delete_table(u'metrics_social_insightsfacebookpageweekly')

        # Deleting model 'InsightsFacebookPost'
        db.delete_table(u'metrics_social_insightsfacebookpost')


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
        u'metrics_social.insightsfacebookpagedaily': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'InsightsFacebookPageDaily'},
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
        u'metrics_social.insightsfacebookpagedays28': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'InsightsFacebookPageDays28'},
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
        u'metrics_social.insightsfacebookpageweekly': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'InsightsFacebookPageWeekly'},
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
        u'metrics_social.insightsfacebookpost': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'InsightsFacebookPost'},
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