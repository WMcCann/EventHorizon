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
from services_social.models import YoutubeConnection
from social.models import AdvertiserYoutubeChannel
from metrics_social.models import YoutubeVideo, EvolutionYoutubeChannel

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<advertiseryoutubechannel_id advertiseryoutubechannel_id ...>'
    help = 'Load videos from all channels'

    def handle(self, *args, **options):
        try:
            ytc = YoutubeConnection.objects.filter(deleted=False)[0]
        except IndexError:
            self.stdout.write(u'Error: there is no YoutubeConnection')
            ytc = None

        if ytc:
            storage = Storage(YoutubeConnection, 'email', ytc.email, 'credential')
            credential = storage.get()
            if credential is None or credential.invalid == True:
                CommandError(u'YoutubeConnection is invalid')

            http = httplib2.Http()
            http = credential.authorize(http)
            service = build('youtube', 'v3', http=http)


            if args:
                aycs = AdvertiserYoutubeChannel.objects.filter(youtube_id__in=args, first_load=False, deleted=False)
            else:
                aycs = AdvertiserYoutubeChannel.objects.filter(first_load=False, deleted=False)

            # do first load
            for ayc in [a for a in aycs]:
                channels = service.channels().list(part='statistics', id=ayc.youtube_id).execute()

                ayc.views_count = channels[u'items'][0][u'statistics'][u'viewCount']
                ayc.videos_count = channels[u'items'][0][u'statistics'][u'videoCount']
                ayc.subscribers_count = channels[u'items'][0][u'statistics'][u'subscriberCount']
                ayc.save()

                evolution = EvolutionYoutubeChannel(
                    youtube_channel=ayc,
                    views_count=channels[u'items'][0][u'statistics'][u'viewCount'],
                    videos_count=channels[u'items'][0][u'statistics'][u'videoCount'],
                    subscribers_count=channels[u'items'][0][u'statistics'][u'subscriberCount'],
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Advertiser Youtube Channel: %s \n\n' % ayc.youtube_id)

                main_loop = True
                try:
                    page_token = APIPagination.objects.get(
                        app_name=u'metrics_social',
                        model_name='YoutubeVideo',
                        path=u'/%s/video' % ayc.youtube_id,
                        ).offset
                except APIPagination.DoesNotExist:
                    page_token = None

                while main_loop:
                    search = service.search().list(
                        part='id',
                        channelId=ayc.youtube_id,
                        maxResults=50,
                        order='date',
                        pageToken=page_token,
                        type='video',
                        ).execute()

                    items = [item[u'id'][u'videoId'] for item in search[u'items'] 
                             if item[u'kind'] == u'youtube#searchResult' and item[u'id'][u'kind'] == u'youtube#video']

                    videos = service.videos().list(
                        part='id,snippet,statistics',
                        id=','.join(items),
                        maxResults=50,
                        ).execute()

                    page_save = PageSave('metrics_social', 'YoutubeVideo')
                    page_save.start_save(videos[u'items'], yc=ayc)

                    if u'nextPageToken' in search:
                        page_token = search[u'nextPageToken']
                        self.stdout.write(u'Going to next page \n\n\n')

                        try:
                            stopped_at = APIPagination.objects.get(
                                app_name=u'metrics_social',
                                model_name='YoutubeVideo',
                                path=u'/%s/video' % ayc.youtube_id,
                                )
                            stopped_at.offset = page_token
                            stopped_at.save()
                        except APIPagination.DoesNotExist:
                            stopped_at = APIPagination(
                                app_name=u'metrics_social',
                                model_name='YoutubeVideo',
                                path=u'/%s/video' % ayc.youtube_id,
                                offset=page_token,
                                )
                            stopped_at.save()
                    else:
                        main_loop = False
                        ayc.first_load = True
                        ayc.save()