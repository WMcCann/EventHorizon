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
from metrics_social.models import TwitterMessage, EvolutionTwitterProfile


class Command(BaseCommand):
    args = '<campaigntwitterprofile_id campaigntwitterprofile_id ...>'
    help = 'Load tweets from all profiles'

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

                page = 1

                main_loop = True
                while main_loop:
                    statuses = api.user_timeline(user_id=ctp.twitter_id, page=page, count=200)
                    if statuses:
                        for status in statuses:
                            try:
                                twm = TwitterMessage.objects.get(
                                    twitter_profile=ctp,
                                    twitter_id__exact=status.id_str,
                                    deleted=False,
                                    )
                            except TwitterMessage.DoesNotExist:
                                try:
                                    twm = TwitterMessage(
                                        twitter_profile=ctp,
                                        twitter_id=status.id_str,
                                        author_twitter_id=status.author.id_str,
                                        message=status.text,
                                        created_time=status.created_at,
                                        favorites=status.favorite_count,
                                        retweets=status.retweet_count,
                                        )
                                except Exception, e:
                                    err = APIError(
                                        app_name=u'metrics_social',
                                        model_name='TwitterMessage',
                                        error=u'%s: %s' % (Exception, str(e)),
                                        response=status.id_str,
                                        )
                                    err.save()
                                    self.stdout.write(u'Inserted error message: %s %s' % (Exception, str(e)))
                                else:
                                    twm.save()
                                    self.stdout.write(u'Inserted message %s' % twm.twitter_id)

                            else:
                                self.stdout.write(u'Message already exists: %s' % twm.twitter_id)
                                main_loop = False
                                break

                        page += 1  # next page

                        self.stdout.write(u'Going to next page: %s\n\n' % page)
                    else:
                        main_loop = False