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
from social.models import AdvertiserTwitterProfile
from metrics_social.models import TwitterMessage, EvolutionTwitterProfile


class Command(BaseCommand):
    args = '<advertisertwitterprofile_id advertisertwitterprofile_id ...>'
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
                atps = AdvertiserTwitterProfile.objects.filter(twitter_id__in=args, first_load=True, deleted=False)
            else:
                atps = AdvertiserTwitterProfile.objects.filter(first_load=True, deleted=False)

            error = False
            # do first load
            for atp in [a for a in atps]:
                profile = api.get_user(id=atp.twitter_id)

                atp.name = profile.name
                atp.screen_name = profile.screen_name
                atp.followers_count = profile.followers_count
                atp.friends_count = profile.friends_count
                atp.listed_count = profile.listed_count
                atp.favourites_count = profile.favourites_count
                atp.statuses_count = profile.statuses_count

                atp.save()

                evolution = EvolutionTwitterProfile(
                    twitter_profile=atp,
                    followers_count=atp.followers_count,
                    friends_count=atp.friends_count,
                    listed_count=atp.listed_count,
                    favourites_count=atp.favourites_count,
                    statuses_count=atp.statuses_count,
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Advertiser Twitter Profile: %s \n\n' % atp.twitter_id)

                page = 1

                main_loop = True
                while main_loop:
                    statuses = api.user_timeline(user_id=atp.twitter_id, page=page, count=200)
                    if statuses:
                        for status in statuses:
                            try:
                                twm = TwitterMessage.objects.get(
                                    twitter_profile=atp,
                                    twitter_id__exact=status.id_str,
                                    deleted=False,
                                    )
                            except TwitterMessage.DoesNotExist:
                                try:
                                    twm = TwitterMessage(
                                        twitter_profile=atp,
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