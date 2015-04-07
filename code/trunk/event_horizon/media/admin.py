#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from media.models import *


class AdwordsAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(AdwordsAccount, AdwordsAccountAdmin)