#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import datetime
import urlparse
import logging

from collections import OrderedDict

from django.db import connection, transaction
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from third_party.facebook.facebook import FacebookClient
from third_party.facebook.exceptions import FacebookGenericError

from core.models import Person, APIError, APIPagination
from services_social.models import FacebookConnection
from social.models import FacebookUser, InsightsFacebookPage
from metrics_social.models import FacebookMessage, EvolutionFacebookPageLike, InsightsMetric

from core.utils import BulkInsertOrUpdate
from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<facebookpage_id facebookpage_id ...>'
    help = 'Load insights from all postss'

    def handle(self, *args, **options):
        # get some access_token
        try:
            fbc = FacebookConnection.objects.filter(expires__gt=datetime.datetime.now(), deleted=False)[0]
        except IndexError:
            self.stdout.write(u'Error: there is no FacebookConnection')
            fbc = None

        if fbc:
            metrics = [
                u'post_stories',
                u'post_storytellers',
                u'post_impressions',
                u'post_impressions_unique',
                u'post_impressions_paid',
                u'post_impressions_paid_unique',
                u'post_impressions_fan',
                u'post_impressions_fan_unique',
                u'post_impressions_fan_paid',
                u'post_impressions_fan_paid_unique',
                u'post_impressions_organic',
                u'post_impressions_organic_unique',
                u'post_impressions_viral',
                u'post_impressions_viral_unique',
                u'post_consumptions',
                u'post_consumptions_unique',
                u'post_engaged_users',
                u'post_negative_feedback',
                u'post_negative_feedback_unique',
                ]

            fields = OrderedDict([
                (u'facebook_message_id', u'INT'),
                (u'facebook_page_id', u'INT'),
                (u'metric', u'NVARCHAR(255)'),
                (u'period', u'NVARCHAR(255)'),
                (u'value', u'BIGINT'),
                (u'title', u'NVARCHAR(255)'),
                (u'description', u'NVARCHAR(MAX)'),
                ])

            # api client
            client = FacebookClient(
                client_id=settings.FB_CLIENT_ID, 
                client_secret=settings.FB_CLIENT_SECRET,
                access_token=fbc.access_token,
                )

            # do first load
            if args:
                ifps = [i for i in InsightsFacebookPage.objects.filter(
                                        facebook_page__facebook_id__in=args, 
                                        deleted=False)]
            else:
                ifps = [i for i in InsightsFacebookPage.objects.filter(deleted=False)]

            error = False
            for ifp in ifps:
                if error:
                    break

                # page info
                try:
                    ifp_info = client.obj_id(ifp.facebook_page.facebook_id)
                except FacebookGenericError:
                    if FacebookGenericError.code == u'17':
                        fbc, access_token = FacebookConnection.renew_client(fbc)
                        client._access_token = access_token
                        ifp_info = client.obj_id(ifp.facebook_page.facebook_id)
                else:
                    if not ifp_info:
                        fbc, access_token = FacebookConnection.renew_client(fbc)
                        client._access_token = access_token
                        ifp_info = client.obj_id(ifp.facebook_page.facebook_id)

                    if not ifp_info:
                        error = True
                        continue
                        #raise CommandError(u'\nThe limit of all robots was reached.')

                ifp.facebook_page.name = ifp_info[u'name']
                ifp.facebook_page.link = ifp_info[u'link']
                ifp.facebook_page.talking_about = ifp_info[u'talking_about_count']
                ifp.facebook_page.likes = ifp_info[u'likes']

                ifp.facebook_page.save()

                evolution = EvolutionFacebookPageLike(
                    facebook_page=ifp.facebook_page,
                    likes=ifp_info[u'likes'],
                    )
                evolution.save()

                self.stdout.write(u'Successfully updated Facebook Page: %s \n\n' % ifp.facebook_page.facebook_id)

                already_exists = [x for x in InsightsMetric.objects.values_list(
                        'facebook_message_id', 
                        flat=True,
                    ).filter(
                        facebook_page=ifp,
                        metric__in=metrics,
                        dimension=None,
                        deleted=False,
                    ) if x]


                end_date = datetime.date.today()
                end_date = datetime.date.fromordinal(end_date.toordinal() - 2)
                fbmsgs = [y for y in FacebookMessage.objects.filter(
                        facebook_page=ifp.facebook_page,
                        author_facebook_id=ifp.facebook_page.facebook_id,
                        created_time__lte=datetime.datetime.combine(end_date, datetime.time()),
                        deleted=False,
                    ) if y.id not in already_exists or \
                        y.created_time > datetime.datetime.combine(
                            datetime.date.fromordinal(end_date.toordinal() - 3), datetime.time()
                            )]

                for fbmsg in fbmsgs:
                    if error:
                        break

                    fbmsgs_tasks = []
                    for metric in metrics:
                        path = u'/%s/insights/%s/lifetime' % (fbmsg.facebook_id, metric)
                        fbmsgs_tasks.append({
                            u'id': path,
                            u'path': path,
                            u'args': [],
                            u'kwargs': {},
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

                    rows = []
                    for task in client.tasks:
                        if u'response' in task:
                            if not u'data' in task[u'response']:
                                continue
                            for data in task[u'response'][u'data']:
                                for row in data[u'values']:
                                    rows.append((
                                        fbmsg.id,
                                        ifp.id,
                                        str(data[u'name']),
                                        str(data[u'period']),
                                        row[u'value'],
                                        str(data[u'title']),
                                        str(data[u'description'])
                                        ))

                            if not len(task[u'response'][u'data']):
                                rows.append((
                                    fbmsg.id,
                                    ifp.id,
                                    str(task[u'path'].split('/')[3]),
                                    str(u'Not provided'),
                                    0,
                                    str(u'Not provided'),
                                    str(u'Not provided')
                                    ))


                    if rows:
                        bk = BulkInsertOrUpdate(fields=fields)
                        matches = [{
                            u'clause': None,
                            u'first_field': u'facebook_message_id',
                            u'comparison': u'=',
                            u'second_field': u'facebook_message_id'
                            },{
                            u'clause': u'AND',
                            u'first_field': u'facebook_page_id',
                            u'comparison': u'=',
                            u'second_field': u'facebook_page_id'
                            },{
                            u'clause': u'AND',
                            u'first_field': u'metric',
                            u'comparison': u'=',
                            u'second_field': u'metric'
                            },{
                            u'clause': u'AND',
                            u'first_field': u'period',
                            u'comparison': u'=',
                            u'second_field': u'period'
                            },]

                        insert_fields = [
                            u'facebook_message_id',
                            u'facebook_page_id',
                            u'metric',
                            u'period',
                            u'value',
                            u'title',
                            u'description'
                            ]

                        cursor = connection.cursor()
                        cursor.execute(
                            bk.bulk(
                                u'SET QUOTED_IDENTIFIER OFF;',
                                bk.command_bulk_create(),
                                bk.command_bulk_insert(rows),
                                bk.command_bulk_merge(
                                    u'metrics_social_insightsmetric',
                                    matches,
                                    [u'value'],
                                    insert_fields
                                    )
                                )
                            )
                        cursor.execute(bk.command_drop_action_table())
                        transaction.commit_unless_managed()


                    self.stdout.write(u'Facebook insights block was created\n')