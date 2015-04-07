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
from social.models import FacebookUser, CampaignFacebookPage
from metrics_social.models import FacebookMessage, FacebookComment, FacebookLike, EvolutionFacebookPageLike

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<campaignfacebookpage_id campaignfacebookpage_id ...>'
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
                cfps = CampaignFacebookPage.objects.filter(facebook_id__in=args, first_load=False, deleted=False)
            else:
                cfps = CampaignFacebookPage.objects.filter(first_load=False, deleted=False)

            error = False
            # do first load
            for cfp in [c for c in cfps]:
                if error:
                    break

                # page info
                try:
                    cfp_info = client.obj_id(cfp.facebook_id)
                except FacebookGenericError:
                    if FacebookGenericError.code == u'17':
                        fbc, access_token = FacebookConnection.renew_client(fbc)
                        client._access_token = access_token
                        cfp_info = client.obj_id(cfp.facebook_id)
                else:
                    if not cfp_info:
                        fbc, access_token = FacebookConnection.renew_client(fbc)
                        client._access_token = access_token
                        cfp_info = client.obj_id(cfp.facebook_id)

                    if not cfp_info:
                        error = True
                        continue
                        #raise CommandError(u'\nThe limit of all robots was reached.')

                cfp_info = client.obj_id(cfp.facebook_id)
                cfp.name = cfp_info[u'name']
                cfp.link = cfp_info[u'link']
                cfp.talking_about = cfp_info[u'talking_about_count']
                cfp.likes = cfp_info[u'likes']

                cfp.save()

                evolution = EvolutionFacebookPageLike(
                    facebook_page=cfp,
                    likes=cfp_info[u'likes'],
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Campaign Facebook Page: %s \n\n' % cfp.facebook_id)

                main_loop = True

                try:
                    until = APIPagination.objects.get(
                        app_name=u'metrics_social',
                        model_name='FacebookMessage',
                        path=u'/%s/feed' % cfp.facebook_id,
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
                        feed = client.feed(cfp.facebook_id, **params)
                    except FacebookGenericError:
                        if FacebookGenericError.code == u'17':
                            fbc, access_token = FacebookConnection.renew_client(fbc)
                            client._access_token = access_token
                            feed = client.feed(cfp.facebook_id, **params) 
                    else:
                        if not feed:
                            fbc, access_token = FacebookConnection.renew_client(fbc)
                            client._access_token = access_token
                            feed = client.feed(cfp.facebook_id, **params)

                    if not feed:
                        error = True
                        continue
                        #raise CommandError(u'\nThe limit of all robots was reached.')

                    if not u'data' in feed or not len(feed[u'data']):
                        main_loop = False
                        cfp.first_load = True
                        cfp.save()
                        continue

                    page_save = PageSave('metrics_social', 'FacebookMessage')
                    page_save.start_save(feed[u'data'], fp=cfp)

                    self.stdout.write(u'Facebook message block was created\n')
                    self.stdout.write(u'\n'.join(page_save.responses))

                    if u'paging' in feed and u'next' in feed[u'paging']:
                        until = urlparse.parse_qs(urlparse.urlparse(feed[u'paging'][u'next']).query)[u'until'][0]
                        self.stdout.write(u'Going to next page \n\n\n')

                        try:
                            stopped_at = APIPagination.objects.get(
                                app_name=u'metrics_social',
                                model_name='FacebookMessage',
                                path=u'/%s/feed' % cfp.facebook_id,
                                )
                            stopped_at.offset = until
                            stopped_at.save()
                        except APIPagination.DoesNotExist:
                            stopped_at = APIPagination(
                                app_name=u'metrics_social',
                                model_name='FacebookMessage',
                                path=u'/%s/feed' % cfp.facebook_id,
                                offset=until,
                                )
                            stopped_at.save()
                    else:
                        main_loop = False
                        cfp.first_load = True
                        cfp.save()