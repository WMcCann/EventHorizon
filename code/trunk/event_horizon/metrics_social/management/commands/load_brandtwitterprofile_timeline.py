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
from social.models import BrandTwitterProfile
from metrics_social.models import TwitterMessage, EvolutionTwitterProfile


class Command(BaseCommand):
    args = '<brandtwitterprofile_id brandtwitterprofile_id ...>'
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
                btps = BrandTwitterProfile.objects.filter(twitter_id__in=args, first_load=False, deleted=False)
            else:
                btps = BrandTwitterProfile.objects.filter(first_load=False, deleted=False)

            error = False
            # do first load
            for btp in [b for b in btps]:
                profile = api.get_user(id=btp.twitter_id)

                btp.name = profile.name
                btp.screen_name = profile.screen_name
                btp.followers_count = profile.followers_count
                btp.friends_count = profile.friends_count
                btp.listed_count = profile.listed_count
                btp.favourites_count = profile.favourites_count
                btp.statuses_count = profile.statuses_count

                btp.save()

                evolution = EvolutionTwitterProfile(
                    twitter_profile=btp,
                    followers_count=btp.followers_count,
                    friends_count=btp.friends_count,
                    listed_count=btp.listed_count,
                    favourites_count=btp.favourites_count,
                    statuses_count=btp.statuses_count,
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Brand Twitter Profile: %s \n\n' % btp.twitter_id)

                try:
                    page = APIPagination.objects.get(
                        app_name=u'metrics_social',
                        model_name='TwitterMessage',
                        path=u'/%s/timeline' % btp.twitter_id,
                        ).offset

                    page = int(page)
                except APIPagination.DoesNotExist:
                    page = 1

                main_loop = True
                while main_loop:
                    statuses = api.user_timeline(user_id=btp.twitter_id, page=page, count=200)
                    if statuses:
                        for status in statuses:
                            try:
                                twm = TwitterMessage.objects.get(
                                    twitter_profile=btp,
                                    twitter_id__exact=status.id_str,
                                    deleted=False,
                                    )
                            except TwitterMessage.DoesNotExist:
                                try:
                                    twm = TwitterMessage(
                                        twitter_profile=btp,
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

                        try:
                            stopped_at = APIPagination.objects.get(
                                app_name=u'metrics_social',
                                model_name='TwitterMessage',
                                path=u'/%s/timeline' % btp.twitter_id,
                                )
                            stopped_at.offset = page
                            stopped_at.save()
                        except APIPagination.DoesNotExist:
                            stopped_at = APIPagination(
                                app_name=u'metrics_social',
                                model_name='TwitterMessage',
                                path=u'/%s/timeline' % btp.twitter_id,
                                offset=page,
                                )
                            stopped_at.save()

                        page += 1  # next page

                        self.stdout.write(u'Going to next page: %s\n\n' % page)
                    else:
                        main_loop = False
                        btp.first_load = True
                        btp.save()