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
from social.models import BrandYoutubeChannel
from metrics_social.models import YoutubeVideo, EvolutionYoutubeChannel

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<brandyoutubechannel_id brandyoutubechannel_id ...>'
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
                bycs = BrandYoutubeChannel.objects.filter(youtube_id__in=args, first_load=True, deleted=False)
            else:
                bycs = BrandYoutubeChannel.objects.filter(first_load=True, deleted=False)

            # do first load
            for byc in [b for b in bycs]:
                channels = service.channels().list(part='statistics', id=byc.youtube_id).execute()
                
                if not channels[u'items']:
                    continue

                byc.views_count = channels[u'items'][0][u'statistics'][u'viewCount']
                byc.videos_count = channels[u'items'][0][u'statistics'][u'videoCount']
                byc.subscribers_count = channels[u'items'][0][u'statistics'][u'subscriberCount']
                byc.save()

                evolution = EvolutionYoutubeChannel(
                    youtube_channel=byc,
                    views_count=channels[u'items'][0][u'statistics'][u'viewCount'],
                    videos_count=channels[u'items'][0][u'statistics'][u'videoCount'],
                    subscribers_count=channels[u'items'][0][u'statistics'][u'subscriberCount'],
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Brand Youtube Channel: %s \n\n' % byc.youtube_id)

                main_loop = True
                page_token = None

                while main_loop:
                    search = service.search().list(
                        part='id',
                        channelId=byc.youtube_id,
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

                    for row in videos[u'items']:
                        # saving video
                        if row[u'kind'] == u'youtube#video':
                            try:
                                ytv = YoutubeVideo.objects.get(
                                    youtube_channel=byc,
                                    youtube_id__exact=row[u'id'],
                                    deleted=False,
                                    )
                            except YoutubeVideo.DoesNotExist:
                                try:
                                    ytv = YoutubeVideo(
                                        youtube_channel=byc,
                                        youtube_id=row[u'id'],
                                        title=row[u'snippet'][u'title'],
                                        description=row[u'snippet'][u'description'],
                                        created_time=datetime.datetime.strptime(row[u'snippet'][u'publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z'),
                                        views=row[u'statistics'][u'viewCount'],
                                        likes=row[u'statistics'][u'likeCount'],
                                        dislikes=row[u'statistics'][u'dislikeCount'],
                                        favorites=row[u'statistics'][u'favoriteCount'],
                                        comments=row[u'statistics'][u'commentCount'],
                                        )
                                except Exception, e:
                                    err = APIError(
                                        app_name=u'metrics_social',
                                        model_name='YoutubeVideo',
                                        error=u'%s: %s' % (Exception, str(e)),
                                        response=row,
                                        )
                                    err.save()
                                    self.stdout.write(u'Inserted error video: %s %s' % (Exception, str(e)))
                                else:
                                    ytv.save()
                                    self.stdout.write(u'Inserted video %s' % ytv.youtube_id)
                            else:
                                main_loop = False
                                self.stdout.write(u'Video already exists: %s' % ytv.youtube_id)
                                break

                    if u'nextPageToken' in search:
                        page_token = search[u'nextPageToken']
                    else:
                        main_loop = False