#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('dashboard.views',

    # Connections
    url(r'^$', 'select_brand', name='select_brand'),
    url(r'^(?P<dash_id>\d+)$', 'dashboard', name='dashboard'),
    url(r'^(?P<dash_id>\d+)/customer/(?P<brand_id>\d+)$', 'customer', name='customer'),

)