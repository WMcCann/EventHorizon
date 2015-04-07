#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import httplib2
import datetime
import urlparse
import logging

from oauth2client.django_orm import Storage
from apiclient.discovery import build

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import Person, APIError, APIPagination
from social.models import AnalyticsYoutubeChannel
from metrics_social.models import YoutubeVideo, EvolutionYoutubeChannel

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<youtube_id youtube_id ...>'
    help = 'Load analytics from all pages'

    def handle(self, *args, **options):
        config = {
            u'metrics': [
                u'annotationClickThroughRate',
                u'annotationCloseRate',
                u'averageViewDuration',
                u'comments',
                u'dislikes',
                u'estimatedMinutesWatched',
                u'favoritesAdded',
                u'favoritesRemoved',
                u'likes',
                u'shares',
                u'subscribersGained',
                u'subscribersLost',
                u'views',
                ],
            u'dimensions': [
                u'day',
                ],
            u'start_date': u'2014-03-01',
            u'end_date': u'2014-03-19',
            u'start_index': 1,
            u'max_results': 100,
            }

        if args:
            aycs = AnalyticsYoutubeChannel.objects.filter(
                youtube_channel__youtube_id__in=args, first_load=False, deleted=False)
        else:
            aycs = AnalyticsYoutubeChannel.objects.filter(first_load=False, deleted=False)

        for ayc in aycs:
            storage = Storage(AnalyticsYoutubeChannel, 'email', ayc.email, 'credential')
            credential = storage.get()
            if credential is None or credential.invalid == True:
                CommandError(u'YoutubeConnection is invalid')

            http = httplib2.Http()
            http = credential.authorize(http)
            service = build('youtubeAnalytics', 'v1', http=http)

            analytics_response = service.reports().query(
                ids="channel==%s" % ayc.youtube_channel.youtube_id,
                metrics=u','.join(config[u'metrics']),
                dimensions=u','.join(config[u'dimensions']),
                start_date=config[u'start_date'],
                end_date=config[u'end_date'],
                start_index=config[u'start_index'],
                max_results=config[u'max_results'],
            ).execute()

            for column_header in analytics_response.get("columnHeaders", []):
                print "%-20s" % column_header["name"],

            for row in analytics_response.get("rows", []):
                for value in row:
                    print "%-20s" % value,