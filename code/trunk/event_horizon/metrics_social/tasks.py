#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from datetime import timedelta
from celery.task import periodic_task

from django.core.management import call_command

# Feed tasks

@periodic_task(run_every=timedelta(minutes=15))
def load_brandfacebookpage_feed():
    call_command('load_brandfacebookpage_feed')
    return u'Called load_brandfacebookpage_feed...'


@periodic_task(run_every=timedelta(minutes=15))
def load_advertiserfacebookpage_feed():
    call_command('load_advertiserfacebookpage_feed')
    return u'Called load_advertiserfacebookpage_feed...'


@periodic_task(run_every=timedelta(minutes=15))
def load_campaignfacebookpage_feed():
    call_command('load_campaignfacebookpage_feed')
    return u'Called load_campaignfacebookpage_feed...'


@periodic_task(run_every=timedelta(days=1))
def load_brandfacebookpage_feed_daily():
    call_command('load_brandfacebookpage_feed_daily')
    return u'Called load_brandfacebookpage_feed_daily...'


@periodic_task(run_every=timedelta(days=1))
def load_advertiserfacebookpage_feed_daily():
    call_command('load_advertiserfacebookpage_feed_daily')
    return u'Called load_advertiserfacebookpage_feed_daily...'


@periodic_task(run_every=timedelta(days=1))
def load_campaignfacebookpage_feed_daily():
    call_command('load_campaignfacebookpage_feed_daily')
    return u'Called load_campaignfacebookpage_feed_daily...'


# Comments tasks

@periodic_task(run_every=timedelta(minutes=15))
def load_brandfacebookpage_comments():
    call_command('load_brandfacebookpage_comments')
    return u'Called load_brandfacebookpage_comments...'


@periodic_task(run_every=timedelta(minutes=15))
def load_advertiserfacebookpage_comments():
    call_command('load_advertiserfacebookpage_comments')
    return u'Called load_advertiserfacebookpage_comments...'


@periodic_task(run_every=timedelta(minutes=15))
def load_campaignfacebookpage_comments():
    call_command('load_campaignfacebookpage_comments')
    return u'Called load_campaignfacebookpage_comments...'


# Likes tasks

@periodic_task(run_every=timedelta(minutes=15))
def load_brandfacebookpage_likes():
    call_command('load_brandfacebookpage_likes')
    return u'Called load_brandfacebookpage_likes...'


@periodic_task(run_every=timedelta(minutes=15))
def load_advertiserfacebookpage_likes():
    call_command('load_advertiserfacebookpage_likes')
    return u'Called load_advertiserfacebookpage_likes...'


@periodic_task(run_every=timedelta(minutes=15))
def load_campaignfacebookpage_likes():
    call_command('load_campaignfacebookpage_likes')
    return u'Called load_campaignfacebookpage_likes...'


# Insights tasks

@periodic_task(run_every=timedelta(minutes=15))
def load_insights_facebookpage_daily():
    call_command('load_insights_facebookpage_daily')
    return u'Called load_insights_facebookpage_daily...'


@periodic_task(run_every=timedelta(minutes=15))
def load_insights_facebookpage_weekly():
    call_command('load_insights_facebookpage_weekly')
    return u'Called load_insights_facebookpage_weekly...'


@periodic_task(run_every=timedelta(minutes=15))
def load_insights_facebookpage_days_28():
    call_command('load_insights_facebookpage_days_28')
    return u'Called load_insights_facebookpage_days_28...'


@periodic_task(run_every=timedelta(minutes=15))
def load_insights_facebookpage_dimensions():
    call_command('load_insights_facebookpage_dimensions')
    return u'Called load_insights_facebookpage_dimensions...'


@periodic_task(run_every=timedelta(minutes=15))
def load_insights_facebookpage_by_message():
    call_command('load_insights_facebookpage_by_message')
    return u'Called load_insights_facebookpage_by_message...'


@periodic_task(run_every=timedelta(minutes=15))
def load_insights_facebookpage_dimensions_by_message():
    call_command('load_insights_facebookpage_dimensions_by_message')
    return u'Called load_insights_facebookpage_dimensions_by_message...'


@periodic_task(run_every=timedelta(days=1))
def load_insights_facebookpage_daily_daily():
    call_command('load_insights_facebookpage_daily_daily')
    return u'Called load_insights_facebookpage_daily_daily...'


@periodic_task(run_every=timedelta(days=1))
def load_insights_facebookpage_weekly_daily():
    call_command('load_insights_facebookpage_weekly_daily')
    return u'Called load_insights_facebookpage_weekly_daily...'


@periodic_task(run_every=timedelta(days=15))
def load_insights_facebookpage_days_28_daily():
    call_command('load_insights_facebookpage_days_28_daily')
    return u'Called load_insights_facebookpage_days_28_daily...'


@periodic_task(run_every=timedelta(days=1))
def load_insights_facebookpage_dimensions_daily():
    call_command('load_insights_facebookpage_dimensions_daily')
    return u'Called load_insights_facebookpage_dimensions_daily...'


# Update

@periodic_task(run_every=timedelta(hours=1))
def update_brandfacebookpage_comments():
    call_command('update_brandfacebookpage_comments')
    return u'Called update_brandfacebookpage_comments...'


@periodic_task(run_every=timedelta(hours=1))
def update_advertiserfacebookpage_comments():
    call_command('update_advertiserfacebookpage_comments')
    return u'Called update_advertiserfacebookpage_comments...'


@periodic_task(run_every=timedelta(hours=1))
def update_campaignfacebookpage_comments():
    call_command('update_campaignfacebookpage_comments')
    return u'Called update_campaignfacebookpage_comments...'


@periodic_task(run_every=timedelta(hours=1))
def update_brandfacebookpage_likes():
    call_command('update_brandfacebookpage_likes')
    return u'Called update_brandfacebookpage_likes...'


@periodic_task(run_every=timedelta(hours=1))
def update_advertiserfacebookpage_likes():
    call_command('update_advertiserfacebookpage_likes')
    return u'Called update_advertiserfacebookpage_likes...'


@periodic_task(run_every=timedelta(hours=1))
def update_campaignfacebookpage_likes():
    call_command('update_campaignfacebookpage_likes')
    return u'Called update_campaignfacebookpage_likes...'


@periodic_task(run_every=timedelta(hours=1))
def update_brandfacebookpage_shares():
    call_command('update_brandfacebookpage_shares')
    return u'Called update_brandfacebookpage_shares...'


@periodic_task(run_every=timedelta(hours=1))
def update_advertiserfacebookpage_shares():
    call_command('update_advertiserfacebookpage_shares')
    return u'Called update_advertiserfacebookpage_shares...'


@periodic_task(run_every=timedelta(hours=1))
def update_campaignfacebookpage_shares():
    call_command('update_campaignfacebookpage_shares')
    return u'Called update_campaignfacebookpage_shares...'


# Twitter tasks

@periodic_task(run_every=timedelta(minutes=20))
def load_advertisertwitterprofile_timeline():
    call_command('load_advertisertwitterprofile_timeline')
    return u'Called load_advertisertwitterprofile_timeline...'


@periodic_task(run_every=timedelta(minutes=20))
def load_brandtwitterprofile_timeline():
    call_command('load_brandtwitterprofile_timeline')
    return u'Called load_brandtwitterprofile_timeline...'


@periodic_task(run_every=timedelta(minutes=20))
def load_campaigntwitterprofile_timeline():
    call_command('load_campaigntwitterprofile_timeline')
    return u'Called load_campaigntwitterprofile_timeline...'


@periodic_task(run_every=timedelta(minutes=20))
def load_advertisertwitterprofile_retweets():
    call_command('load_advertisertwitterprofile_retweets')
    return u'Called load_advertisertwitterprofile_retweets...'


@periodic_task(run_every=timedelta(minutes=20))
def load_brandtwitterprofile_retweets():
    call_command('load_brandtwitterprofile_retweets')
    return u'Called load_brandtwitterprofile_retweets...'


@periodic_task(run_every=timedelta(minutes=20))
def load_campaigntwitterprofile_retweets():
    call_command('load_campaigntwitterprofile_retweets')
    return u'Called load_campaigntwitterprofile_retweets...'


@periodic_task(run_every=timedelta(days=1))
def load_advertisertwitterprofile_timeline_daily():
    call_command('load_advertisertwitterprofile_timeline_daily')
    return u'Called load_advertisertwitterprofile_timeline_daily...'


@periodic_task(run_every=timedelta(days=1))
def load_brandtwitterprofile_timeline_daily():
    call_command('load_brandtwitterprofile_timeline_daily')
    return u'Called load_brandtwitterprofile_timeline_daily...'


@periodic_task(run_every=timedelta(days=1))
def load_campaigntwitterprofile_timeline_daily():
    call_command('load_campaigntwitterprofile_timeline_daily')
    return u'Called load_campaigntwitterprofile_timeline_daily...'