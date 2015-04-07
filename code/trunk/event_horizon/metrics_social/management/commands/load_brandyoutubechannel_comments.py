#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import httplib2
import datetime
import urlparse
import logging
import gdata.youtube
import gdata.youtube.service

from urllib import urlencode
from oauth2client.django_orm import Storage
from apiclient.discovery import build

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import Person, APIError, APIPagination
from services_social.models import YoutubeConnection
from social.models import BrandYoutubeChannel
from metrics_social.models import YoutubeVideo, EvolutionYoutubeChannel, YoutubeComment

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<brandyoutubechannel_id brandyoutubechannel_id ...>'
    help = 'Load comments from all videos'

    def handle(self, *args, **options):
        base_url = u'http://gdata.youtube.com/feeds/api/videos/'
        yt_service = gdata.youtube.service.YouTubeService()

        if args:
            bycs = BrandYoutubeChannel.objects.filter(youtube_id__in=args, first_load=True, deleted=False)
        else:
            bycs = BrandYoutubeChannel.objects.filter(first_load=True, deleted=False)

        error = False
        for byc in [b for b in bycs]:
            if error:
                break

            ytvs = YoutubeVideo.objects.filter(
                youtube_channel=byc,
                loaded_comments=False,
                deleted=False,
                ).order_by('-created_time')

            for ytv in [y for y in ytvs]:
                # get pagination
                try:
                    start_index = APIPagination.objects.get(
                    app_name=u'metrics_social',
                    model_name=u'YoutubeComment',
                    path=u'/%s/comments' % (ytv.youtube_id),
                    ).offset
                except APIPagination.DoesNotExist:
                    start_index = None


                if not start_index:
                    url = base_url + (u'%s/comments' % ytv.youtube_id)
                    try:
                        feed = yt_service.GetYouTubeVideoCommentFeed(uri=url)
                    except Exception, e:
                        ytv.loaded_comments = True
                        ytv.save()
                        feed = None
                        self.stdout.write(u'Error when load feed: %s %s' % (Exception, str(e)))
                else:
                    params = {
                        u'start-index': start_index,
                        u'max-results': '25',
                        u'direction': 'next',
                        }

                    url = base_url + (u'%s/comments' % ytv.youtube_id) + urlencode(params)

                    try:
                        feed = yt_service.Query(url)
                    except Exception, e:
                        ytv.loaded_comments = True
                        ytv.save()
                        feed = None
                        self.stdout.write(u'Error when load feed: %s %s' % (Exception, str(e)))

                while feed:
                    for entry in feed.entry:
                        _id = entry.id.text.split('/')[-1]
                        _username = entry.author[0].uri.text.split('/')[-1].decode('utf8')

                        try:
                            _title = entry.title.text.decode('utf8')
                        except Exception, e:
                            _title = ''

                        try:
                            _comment = entry.content.text.decode('utf8')
                        except Exception, e:
                            _comment = ''

                        _created_time = datetime.datetime.strptime(entry.published.text, '%Y-%m-%dT%H:%M:%S.000Z')

                        try:
                            ytc = YoutubeComment.objects.get(
                                video=ytv,
                                youtube_id__exact=_id,
                                deleted=False
                                )
                        except YoutubeComment.DoesNotExist:
                            try:
                                ytc = YoutubeComment(
                                    youtube_id=_id,
                                    video=ytv,
                                    author_youtube_username=_username,
                                    title=_title,
                                    comment=_comment,
                                    created_time=_created_time,
                                    )
                            except Exception, e:
                                err = APIError(
                                    app_name=u'metrics_social',
                                    model_name='YoutubeComment',
                                    error=u'%s: %s' % (Exception, e),
                                    response=entry,
                                    )
                                err.save()
                                self.stdout.write(u'Inserted error comment: %s %s' % (Exception, str(e)))
                            else:
                                ytc.save()
                                self.stdout.write(u'Inserted comment %s' % ytc.youtube_id)
                        else:
                            self.stdout.write(u'Comment already exists: %s' % ytc.youtube_id)

                    if feed.GetNextLink():
                        start_index = urlparse.parse_qs(urlparse.urlparse(feed.GetNextLink().href).query)

                        if not u'start-index' in start_index:
                            try:
                                feed = yt_service.Query(feed.GetNextLink().href)
                            except Exception, e:
                                ytv.loaded_comments = True
                                ytv.save()
                                feed = None
                                self.stdout.write(u'Error when load feed: %s %s' % (Exception, str(e)))
                            continue

                        stopped_at, created = APIPagination.objects.get_or_create(
                            app_name=u'metrics_social',
                            model_name=u'YoutubeComment',
                            path=u'/%s/comments' % (ytv.youtube_id), 
                            defaults={
                                'offset': start_index[u'start-index'][0],
                                }
                            )

                        stopped_at.offset = start_index[u'start-index'][0]
                        stopped_at.save()

                        self.stdout.write(u'Saved pagination for %s\n' % ytv.youtube_id)

                        try:
                            feed = yt_service.Query(feed.GetNextLink().href)
                        except Exception, e:
                            ytv.loaded_comments = True
                            ytv.save()
                            feed = None
                            self.stdout.write(u'Error when load feed: %s %s' % (Exception, str(e)))
                    else:
                        feed = None
                        ytv.loaded_comments = True
                        ytv.save()
