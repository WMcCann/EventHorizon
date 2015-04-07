#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import urlparse
import logging
import tweepy

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import Person, APIError, APIPagination
from services_social.models import TwitterConnection
from social.models import CampaignTwitterProfile
from metrics_social.models import TwitterMessage, TwitterRetweet, EvolutionTwitterProfile


class Command(BaseCommand):
    args = '<campaigntwitterprofile_id campaigntwitterprofile_id ...>'
    help = 'Load retweets from all profiles'

    def handle(self, *args, **options):
        try:
            twc = TwitterConnection.objects.filter(deleted=False)[0]
        except IndexError:
            self.stdout.write(u'Error: there is no TwitterConnection')
            twc = None

        if twc:

            # api client
            auth = tweepy.OAuthHandler(
                settings.TW_CONSUMER_KEY, 
                settings.TW_CONSUMER_SECRET,
                )
            auth.set_access_token(twc.access_token, twc.access_token_secret)
            api = tweepy.API(auth)

            if args:
                ctps = CampaignTwitterProfile.objects.filter(twitter_id__in=args, first_load=True, deleted=False)
            else:
                ctps = CampaignTwitterProfile.objects.filter(first_load=True, deleted=False)

            error = False
            # do first load
            for ctp in [c for c in ctps]:
                profile = api.get_user(id=ctp.twitter_id)

                ctp.name = profile.name
                ctp.screen_name = profile.screen_name
                ctp.followers_count = profile.followers_count
                ctp.friends_count = profile.friends_count
                ctp.listed_count = profile.listed_count
                ctp.favourites_count = profile.favourites_count
                ctp.statuses_count = profile.statuses_count

                ctp.save()

                evolution = EvolutionTwitterProfile(
                    twitter_profile=ctp,
                    followers_count=ctp.followers_count,
                    friends_count=ctp.friends_count,
                    listed_count=ctp.listed_count,
                    favourites_count=ctp.favourites_count,
                    statuses_count=ctp.statuses_count,
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Campaign Twitter Profile: %s \n\n' % ctp.twitter_id)

                end_date = datetime.date.today()
                end_date = datetime.date.fromordinal(end_date.toordinal() - 1)
                statuses = TwitterMessage.objects.filter(
                    twitter_profile=ctp,
                    created_time__lte=datetime.datetime.combine(end_date, datetime.time()),
                    loaded_retweets=False,
                    deleted=False,
                    ).order_by('-created_time')

                for status in [s for s in statuses]:
                    if status.retweets > 0:
                        objs = api.retweets(id=status.twitter_id, count=100)
                        for obj in objs:
                            try:
                                twr, created = TwitterRetweet.objects.get_or_create(
                                    message=status,
                                    author_twitter_id=obj.author.id_str,
                                    defaults={
                                        'created_time': obj.created_at,
                                        },
                                    )
                                twr.save()
                                self.stdout.write(u'Inserted retweet %s' % obj.id_str)
                            except Exception, e:
                                err = APIError(
                                    app_name=u'metrics_social',
                                    model_name='TwitterRetweet',
                                    error=u'%s: %s' % (Exception, str(e)),
                                    response=obj.id_str,
                                    )
                                err.save()
                                self.stdout.write(u'Inserted error message: %s %s' % (Exception, str(e)))

                        status.loaded_retweets = True
                        status.save()
                    else:
                        status.loaded_retweets = True
                        status.save()