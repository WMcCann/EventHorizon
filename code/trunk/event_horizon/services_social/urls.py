#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('services_social.views',

    # Connections
    url(r'^facebook-connection/add/$','facebook_connection_add'),
    url(r'^facebook-connection/oauth/$','facebook_connection_oauth'),

    url(r'^twitter-connection/add/$','twitter_connection_add'),
    url(r'^twitter-connection/oauth/$','twitter_connection_oauth'),

    url(r'^youtube-connection/add/$','youtube_connection_add'),
    url(r'^youtube-connection/oauth/$','youtube_connection_oauth'),


)