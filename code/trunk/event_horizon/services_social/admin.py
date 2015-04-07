#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from services_social.models import *


class ServiceConnectionAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/public/lib/js/jquery-1.10.2.min.js',
            '/public/js/admin.js',
            )

class FacebookConnectionAdmin(ServiceConnectionAdmin):
    pass

class TwitterConnectionAdmin(ServiceConnectionAdmin):
    pass

class YoutubeConnectionAdmin(ServiceConnectionAdmin):
    pass


admin.site.register(FacebookConnection, FacebookConnectionAdmin)
admin.site.register(TwitterConnection, TwitterConnectionAdmin)
admin.site.register(YoutubeConnection, YoutubeConnectionAdmin)