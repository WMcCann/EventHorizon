#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'event_horizon.views.home', name='home'),
    # url(r'^event_horizon/', include('event_horizon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Root redirect to admin
    url(r'^$', RedirectView.as_view(url='/dashboard/'), name='root-admin'),

    # Apps urls
    url(r'^services/social/', include('services_social.urls')),
    url(r'^services/media/', include('services_media.urls')),
    url(r'^social/', include('social.urls')),

    # Dash
    url(r'^dashboard/', include('dashboard.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)