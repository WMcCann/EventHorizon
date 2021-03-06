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

from core.models import Person, APIError, APIPagination
from services_social.models import FacebookConnection
from social.models import FacebookUser, BrandFacebookPage
from metrics_social.models import FacebookMessage, FacebookComment, FacebookLike, EvolutionFacebookPageLike

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<brandfacebookpage_id brandfacebookpage_id ...>'
    help = 'Load feed from all pages'

    def handle(self, *args, **options):
        # get some access_token
        try:
            fbc = FacebookConnection.objects.filter(expires__gt=datetime.datetime.now(), deleted=False)[0]
        except IndexError:
            self.stdout.write(u'Error: there is no FacebookConnection')
            fbc = None

        if fbc:

            # api client
            client = FacebookClient(
                client_id=settings.FB_CLIENT_ID, 
                client_secret=settings.FB_CLIENT_SECRET,
                access_token=fbc.access_token,
                )

            if args:
                bfps = BrandFacebookPage.objects.filter(facebook_id__in=args, first_load=False, deleted=False)
            else:
                bfps = BrandFacebookPage.objects.filter(first_load=False, deleted=False)

            error = False
            # do first load
            for bfp in [b for b in bfps]:
                if error:
                    break

                # page info
                try:
                    bfp_info = client.obj_id(bfp.facebook_id)
                except FacebookGenericError:
                    if FacebookGenericError.code == u'17':
                        fbc, access_token = FacebookConnection.renew_client(fbc)
                        client._access_token = access_token
                        bfp_info = client.obj_id(bfp.facebook_id)
                else:
                    if not bfp_info:
                        fbc, access_token = FacebookConnection.renew_client(fbc)
                        client._access_token = access_token
                        bfp_info = client.obj_id(bfp.facebook_id)

                    if not bfp_info:
                        error = True
                        continue
                        #raise CommandError(u'\nThe limit of all robots was reached.')

                bfp_info = client.obj_id(bfp.facebook_id)
                bfp.name = bfp_info[u'name']
                bfp.link = bfp_info[u'link']
                bfp.talking_about = bfp_info[u'talking_about_count']
                bfp.likes = bfp_info[u'likes']

                bfp.save()

                evolution = EvolutionFacebookPageLike(
                    facebook_page=bfp,
                    likes=bfp_info[u'likes'],
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Brand Facebook Page: %s \n\n' % bfp.facebook_id)

                main_loop = True

                try:
                    until = APIPagination.objects.get(
                        app_name=u'metrics_social',
                        model_name='FacebookMessage',
                        path=u'/%s/feed' % bfp.facebook_id,
                        ).offset
                except APIPagination.DoesNotExist:
                    until = None

                while main_loop:
                    if error:
                        break

                    params = {
                        u'limit': 50,
                        u'format': u'json',
                        u'method': u'GET',
                        }

                    if until:
                        params.update({u'until': until})

                    try:
                        feed = client.feed(bfp.facebook_id, **params)
                    except FacebookGenericError:
                        if FacebookGenericError.code == u'17':
                            fbc, access_token = FacebookConnection.renew_client(fbc)
                            client._access_token = access_token
                            feed = client.feed(bfp.facebook_id, **params) 
                    else:
                        if not feed:
                            fbc, access_token = FacebookConnection.renew_client(fbc)
                            client._access_token = access_token
                            feed = client.feed(bfp.facebook_id, **params)

                    if not feed:
                        error = True
                        continue
                        #raise CommandError(u'\nThe limit of all robots was reached.')

                    if not u'data' in feed or not len(feed[u'data']):
                        main_loop = False
                        bfp.first_load = True
                        bfp.save()
                        continue

                    page_save = PageSave('metrics_social', 'FacebookMessage')
                    page_save.start_save(feed[u'data'], fp=bfp)

                    self.stdout.write(u'Facebook message block was created\n')
                    self.stdout.write(u'\n'.join(page_save.responses))

                    if u'paging' in feed and u'next' in feed[u'paging']:
                        until = urlparse.parse_qs(urlparse.urlparse(feed[u'paging'][u'next']).query)[u'until'][0]
                        self.stdout.write(u'Going to next page \n\n\n')

                        try:
                            stopped_at = APIPagination.objects.get(
                                app_name=u'metrics_social',
                                model_name='FacebookMessage',
                                path=u'/%s/feed' % bfp.facebook_id,
                                )
                            stopped_at.offset = until
                            stopped_at.save()
                        except APIPagination.DoesNotExist:
                            stopped_at = APIPagination(
                                app_name=u'metrics_social',
                                model_name='FacebookMessage',
                                path=u'/%s/feed' % bfp.facebook_id,
                                offset=until,
                                )
                            stopped_at.save()
                    else:
                        main_loop = False
                        bfp.first_load = True
                        bfp.save()