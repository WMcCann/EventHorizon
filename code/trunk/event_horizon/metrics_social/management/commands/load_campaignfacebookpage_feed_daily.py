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
from social.models import FacebookUser, CampaignFacebookPage
from metrics_social.models import FacebookMessage, FacebookComment, FacebookLike, EvolutionFacebookPageLike

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<campaignfacebookpage_id campaignfacebookpage_id ...>'
    help = 'Daily load of feed from all pages'

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
                cfps = CampaignFacebookPage.objects.filter(facebook_id__in=args, deleted=False)
            else:
                cfps = CampaignFacebookPage.objects.filter(deleted=False)

            error = False
            # do daily load
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

                main_loop = True; until = None
                while main_loop:
                    if error:
                        break

                    params = {u'limit': 50}
                    if until:
                        params.update({u'until': until})

                    # load feed
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
                        cfp.save()
                        continue

                    for row in feed[u'data']:
                        try:
                            fbm = FacebookMessage.objects.get(facebook_id__exact=row[u'id'], deleted=False)
                        except FacebookMessage.DoesNotExist:
                            try:
                                if u'likes' in row and u'count' in row[u'likes']:
                                    likes = row[u'likes'][u'count']
                                else:
                                    likes = 0

                                if u'comments' in row and u'count' in row[u'comments']:
                                    comments = row[u'comments'][u'count']
                                else:
                                    comments = 0

                                content = u''
                                if u'message' in row:
                                    content = u'%s' % row[u'message']

                                if u'story' in row:
                                    content = u'%s %s' % (content, row[u'story'])

                                if u'picture' in row:
                                    content = u'%s %s' % (content, row[u'picture'])

                                if u'link' in row:
                                    content = u'%s %s' % (content, row[u'link'])

                                fbm = FacebookMessage(
                                    facebook_page=cfp,
                                    facebook_id=row[u'id'],
                                    author_facebook_id=row[u'from'][u'id'],
                                    message=content,
                                    created_time=datetime.datetime.strptime(row[u'created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                                    message_type=row[u'type'],
                                    likes=0,
                                    comments=0,
                                    shares=row[u'shares'][u'count'] if u'shares' in row else 0,
                                    )
                            except Exception, e:
                                err = APIError(
                                    app_name=u'metrics_social',
                                    model_name='FacebookMessage',
                                    error=u'%s: %s' % (Exception, str(e)),
                                    response=row,
                                    )
                                err.save()
                                self.stdout.write(u'Inserted error message: %s %s' % (Exception, str(e)))
                            else:
                                fbm.save()
                                self.stdout.write(u'Inserted message %s' % fbm.facebook_id)
                        else:
                            self.stdout.write(u'Message already exists: %s' % fbm.facebook_id)
                            self.stdout.write(u'Stopping...')
                            main_loop = False
                            break

                    if u'paging' in feed and u'next' in feed[u'paging']:
                        until = urlparse.parse_qs(urlparse.urlparse(feed[u'paging'][u'next']).query)[u'until'][0]
                        self.stdout.write(u'Going to next page \n\n\n')
                    else:
                        main_loop = False
                        cfp.save()