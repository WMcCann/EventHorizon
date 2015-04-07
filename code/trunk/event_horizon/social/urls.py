#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('social.views',

    # Analytics
    url(r'^analytics/youtube-channel/add/$','analytics_youtube_channel_add'),
    url(r'^analytics/youtube-channel/oauth/$','analytics_youtube_channel_oauth'),

)