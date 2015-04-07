#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('services_media.views',

    # Connections
    url(r'^adwords-connection/add/$','adwords_connection_add'),
    url(r'^adwords-connection/oauth/$','adwords_connection_oauth'),


)