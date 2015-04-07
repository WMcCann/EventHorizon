#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import json
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from core.models import Sector, Category



class Command(BaseCommand):
    args = ''
    help = 'Load sectors and categories from file in settings'

    def handle(self, *args, **options):

        self.stdout.write(u'Loadding sectors and categories...')

        # load file
        filename = os.path.join(settings.PROJECT_ROOT_PATH, 'event_horizon', 'ibope.json')
        try:
            fp = open(filename, 'r')
            try:
                ibope = json.load(fp)
            finally:
                fp.close()
        except IOError:
            raise CommandError('File not found: "%s"' % filename)

        for sector, categories in ibope.iteritems():
            s, created = Sector.objects.get_or_create(
                name=sector.upper(),
                deleted=False,
                defaults={
                    'mnemonic': sector.upper(),
                    }
                )
            s.save()

            self.stdout.write(u'\nSaved sector %s' % sector)

            for category in categories:
                c, created = Category.objects.get_or_create(
                    name=category[u'category'].upper(),
                    sector=s,
                    deleted=False,
                    defaults={
                        'mnemonic': category[u'category'].upper(),
                        }
                    )
                c.save()

                self.stdout.write(u'\nSaved category %s' % category[u'category'])

