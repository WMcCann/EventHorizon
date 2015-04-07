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
from social.models import FacebookUser, AdvertiserFacebookPage
from metrics_social.models import FacebookMessage, FacebookComment, FacebookLike

from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<advertiserfacebookpage_id advertiserfacebookpage_id ...>'
    help = 'Load comments from all posts'

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
                afps = AdvertiserFacebookPage.objects.filter(facebook_id__in=args, first_load=True, deleted=False)
            else:
                afps = AdvertiserFacebookPage.objects.filter(first_load=True, deleted=False)

            error = False
            for afp in [a for a in afps]:
                if error:
                    break

                # setting params to start loop
                limit = 50
                loop = True

                # start loop
                while loop:
                    if error:
                        break

                    fbmsgs = FacebookMessage.objects.filter(
                        facebook_page=afp,
                        loaded_comments=False,
                        deleted=False,
                        ).order_by('-created_time')[:limit]

                    if not fbmsgs:
                        loop = False
                        continue

                    fbmsgs_tasks = []

                    for fbmsg in [f for f in fbmsgs]:
                        # get comments
                        path = u'/%s/comments' % (fbmsg.facebook_id)

                        # get pagination
                        try:
                            after = APIPagination.objects.get(
                                app_name=u'metrics_social',
                                model_name=u'FacebookComment',
                                path=path,
                                ).offset
                        except APIPagination.DoesNotExist:
                            after = None

                        params = {'limit': '500'}
                        if after:
                            params.update({'after': after})

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

                            if not u'data' in task[u'response']:
                                continue

                            page_save = PageSave('metrics_social', u'FacebookComment')
                            page_save.start_save(task[u'response'][u'data'], fbmowner=owner)

                            owner.comments = FacebookComment.objects.filter(message=owner, deleted=False).count()
                            owner.save()

                            if len(task[u'response'][u'data']) < int(task[u'kwargs'][u'limit']):
                                owner.loaded_comments = True
                                owner.comments = FacebookComment.objects.filter(message=owner, deleted=False).count()
                                owner.save()
                                continue

                            if u'paging' in task[u'response']:
                                after = task[u'response'][u'paging'][u'cursors'][u'after']

                                stopped_at, created = APIPagination.objects.get_or_create(
                                    app_name=u'metrics_social',
                                    model_name=u'FacebookComment',
                                    path=task[u'path'], 
                                    defaults={
                                        'offset': after,
                                        }
                                    )
 
                                stopped_at.offset = after
                                stopped_at.save()

                                self.stdout.write(u'Saved pagination for %s\n' % task[u'path'])

                    self.stdout.write(u'Facebook comment block was created\n')

