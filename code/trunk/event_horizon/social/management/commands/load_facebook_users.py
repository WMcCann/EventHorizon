#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import urlparse
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from third_party.facebook.facebook import FacebookClient
from third_party.facebook.exceptions import FacebookGenericError

from core.models import Person, APIError
from services_social.models import FacebookConnection
from social.models import FacebookUser, BrandFacebookPage
from metrics_social.models import FacebookMessage, FacebookComment, FacebookLike


class Command(BaseCommand):
    args = ''
    help = 'Load all facebook users'

    def handle(self, *args, **options):
    	pass