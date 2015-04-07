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
from metrics_social.models import TwitterMessage, TwitterRetweet, EvolutionTwitterProfile


class Command(BaseCommand):
    args = '<brandtwitterprofile_id brandtwitterprofile_id ...>'
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
                btps = BrandTwitterProfile.objects.filter(twitter_id__in=args, first_load=True, deleted=False)
            else:
                btps = BrandTwitterProfile.objects.filter(first_load=True, deleted=False)

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

                end_date = datetime.date.today()
                end_date = datetime.date.fromordinal(end_date.toordinal() - 1)
                statuses = TwitterMessage.objects.filter(
                    twitter_profile=btp,
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