#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from services_media.models import *


class ServiceConnectionAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/public/lib/js/jquery-1.10.2.min.js',
            '/public/js/admin.js',
            )

class AdwordsConnectionAdmin(ServiceConnectionAdmin):
    pass


admin.site.register(AdwordsConnection, AdwordsConnectionAdmin)