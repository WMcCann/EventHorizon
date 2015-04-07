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
    args = '<brandfacebookpage_id brandfacebookpage_id ...>'
    help = 'Update comments from all posts'

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
                bfps = BrandFacebookPage.objects.filter(facebook_id__in=args, first_load=True, deleted=False)
            else:
                bfps = BrandFacebookPage.objects.filter(first_load=True, deleted=False)

            error = False
            for bfp in [b for b in bfps]:
                if error:
                    break

                # setting params to start loop
                offset = 0
                limit = 100
                loop = True

                since = datetime.date.today()
                since = datetime.date.fromordinal(since.toordinal() - 15)

                # start loop
                updated = []
                while loop:
                    if error:
                        break

                    fbmsgs = FacebookMessage.objects.exclude(
                        id__in=updated,
                        ).filter(
                        facebook_page=bfp,
                        created_time__gte=since,
                        loaded_comments=True,
                        deleted=False,
                        ).order_by('-created_time')[offset:limit]

                    if not fbmsgs:
                        loop = False
                        continue

                    fbmsgs_tasks = []
                    for fbmsg in [f for f in fbmsgs]:
                        path = u'/%s' % (fbmsg.facebook_id)

                        params = {u'fields': u'shares'}

                        fbmsgs_tasks.append({
                            u'id': fbmsg.facebook_id,
                            u'path': path,
                            u'owner': fbmsg,
                            u'args': [],
                            u'kwargs': params,
                            })

                    try:
                        me = client.me()
                    except FacebookGenericError:
                        if FacebookGenericError.code == u'17':
                            fbc, access_token = FacebookConnection.renew_client(fbc)
                            client._access_token = access_token
                    else:
                        if not me:
                            fbc, access_token = FacebookConnection.renew_client(fbc)
                            client._access_token = access_token

                    client.start_async_tasks(fbmsgs_tasks, fbc=fbc)

                    if not all([u'response' in task for task in client.tasks]):
                        error = True
                        continue
                        #raise CommandError(u'\nThe limit of all robots was reached.')

                    for task in client.tasks:
                        if u'response' in task:
                            # task opts
                            owner = task[u'owner']

                            if not u'shares' in task[u'response']:
                                continue

                            owner.shares = task[u'response'][u'shares'][u'count']
                            owner.save()
                            updated.append(owner.id)
                            self.stdout.write(u'Facebook message updated\n')

                    if len(fbmsgs) < limit:
                        loop = False
                    else:
                        offset = offset + limit