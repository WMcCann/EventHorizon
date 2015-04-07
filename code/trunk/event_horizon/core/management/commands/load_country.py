#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import json
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from core.models import Country



class Command(BaseCommand):
    args = ''
    help = 'Load countries from file in settings'

    def handle(self, *args, **options):

        self.stdout.write(u'Loadding countries...')

        # load file
        filename = os.path.join(settings.PROJECT_ROOT_PATH, 'event_horizon', 'countries.json')
        try:
            fp = open(filename, 'r')
            try:
                countries = json.load(fp)
            finally:
                fp.close()
        except IOError:
            raise CommandError('File not found: "%s"' % filename)

        for k, v in countries.iteritems():
            c, created = Country.objects.get_or_create(
                name=v.upper(),
                defaults={
                    'mnemonic': k.upper(),
                    }
                )
            c.mnemonic = k.upper()
            c.save()

            self.stdout.write(u'\nSaved country %s' % v.upper())