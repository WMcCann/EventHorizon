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

from dateutil.relativedelta import relativedelta

from core.models import Person, APIError, APIPagination
from services_social.models import FacebookConnection
from social.models import FacebookUser, InsightsFacebookPage
from metrics_social.models import InsightsMetric, EvolutionFacebookPageLike

from core.utils import BulkInsertOrUpdate
from metrics_social.utils import PageSave


class Command(BaseCommand):
    args = '<facebookpage_id facebookpage_id ...>'
    help = 'Load insights from all pages'

    def handle(self, *args, **options):
        # get some access_token
        try:
            fbc = FacebookConnection.objects.filter(expires__gt=datetime.datetime.now(), deleted=False)[0]
        except IndexError:
            self.stdout.write(u'Error: there is no FacebookConnection')
            fbc = None

        if fbc:
            metrics = [
                u'page_stories',
                u'page_storytellers',
                u'page_impressions',
                u'page_impressions_unique',
                u'page_impressions_paid',
                u'page_impressions_paid_unique',
                u'page_impressions_organic',
                u'page_impressions_organic_unique',
                u'page_impressions_viral',
                u'page_impressions_viral_unique',
                u'page_engaged_users',
                u'page_consumptions',
                u'page_consumptions_unique',
                u'page_negative_feedback',
                u'page_negative_feedback_unique',
                u'page_views_unique',
                u'page_views_login',
                u'page_views_login_unique',
                u'page_posts_impressions',
                u'page_posts_impressions_unique',
                u'page_posts_impressions_paid',
                u'page_posts_impressions_paid_unique',
                u'page_posts_impressions_organic',
                u'page_posts_impressions_organic_unique',
                u'page_posts_impressions_viral',
                u'page_posts_impressions_viral_unique',
                ]

            fields = OrderedDict([
                (u'facebook_page_id', u'INT'),
                (u'day', u'DATETIME'),
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

            if args:
                ifps = [i for i in InsightsFacebookPage.objects.filter(
                                        facebook_page__facebook_id__in=args, 
                                        first_load_weekly=False, 
                                        deleted=False)]
            else:
                ifps = [i for i in InsightsFacebookPage.objects.filter(first_load_weekly=False, deleted=False)]

            error = False
            # do first load
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

                main_loop = True
                lap = 0

                try:
                    since = APIPagination.objects.get(
                        app_name=u'metrics_social',
                        model_name='InsightsMetric',
                        path=u'/%s/insights/page_stories/week' % ifp.facebook_page.facebook_id,
                        ).offset

                    since = int(since)

                    today = datetime.date.today()

                    until = datetime.datetime.fromtimestamp(since).date()

                    if until.month == today.month and until.year == today.year:
                        until = until + relativedelta(days=+(today.day-2))
                        until = int(time.mktime(until.timetuple()))
                    else:
                        until = until + relativedelta(months=+1)
                        until = until + relativedelta(days=-1)
                        until = int(time.mktime(until.timetuple()))

                except APIPagination.DoesNotExist:
                    until = datetime.date.today()
                    until = until + relativedelta(days=-2)
                    since = until + relativedelta(days=-(until.day-1))

                    since = int(time.mktime(since.timetuple()))
                    until = int(time.mktime(until.timetuple()))

                while main_loop:
                    if error:
                        break

                    insights_tasks = []
                    for metric in metrics:

                        path = u'/%s/insights/%s/week' % (ifp.facebook_page.facebook_id, metric)

                        insights_tasks.append({
                            u'id': path,
                            u'path': path,
                            u'args': [],
                            u'kwargs': {'since': since, 'until': until},
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
                            me = client.me()

                        if not me:
                            error = True
                            continue
                            #raise CommandError(u'\nThe limit of all robots was reached.')

                    client.start_async_tasks(insights_tasks, fbc=fbc)

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
                                for row in reversed(data[u'values']):
                                    day = datetime.datetime.strptime(row[u'end_time'][:10], '%Y-%m-%d').date()
                                    day = day + relativedelta(days=-1)

                                    rows.append((
                                        ifp.id,
                                        str(unicode(day)),
                                        str(data[u'name']),
                                        str(data[u'period']),
                                        row[u'value'],
                                        str(data[u'title']),
                                        str(data[u'description'])
                                        ))


                    if rows:
                        bk = BulkInsertOrUpdate(fields=fields)
                        matches = [{
                            u'clause': None,
                            u'first_field': u'facebook_page_id',
                            u'comparison': u'=',
                            u'second_field': u'facebook_page_id'
                            },{
                            u'clause': 'AND',
                            u'first_field': u'day',
                            u'comparison': u'=',
                            u'second_field': u'day'
                            },{
                            u'clause': 'AND',
                            u'first_field': u'metric',
                            u'comparison': u'=',
                            u'second_field': u'metric'
                            },{
                            u'clause': 'AND',
                            u'first_field': u'period',
                            u'comparison': u'=',
                            u'second_field': u'period'
                            },]

                        insert_fields = [
                            u'facebook_page_id',
                            u'day',
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
                    responses = [task[u'response'][u'data'][0] for task in client.tasks if len(task[u'response'][u'data'])]

                    if sum([v[u'value'] for r in responses for v in r[u'values']]):
                        until = datetime.datetime.fromtimestamp(since).date()
                        since = until + relativedelta(months=-1, day=1)
                        until = since + relativedelta(months=+1)
                        
                        since = int(time.mktime(since.timetuple()))
                        until = int(time.mktime(until.timetuple()))

                        self.stdout.write(u'Going to next page \n\n\n')

                        stopped_at, created = APIPagination.objects.get_or_create(
                            app_name=u'metrics_social',
                            model_name=u'InsightsMetric',
                            path=u'/%s/insights/page_stories/week' % ifp.facebook_page.facebook_id, 
                            defaults={
                                'offset': since,
                                }
                            )
 
                        stopped_at.offset = since
                        stopped_at.save()

                    else:
                        lap += 1

                        until = datetime.datetime.fromtimestamp(since).date()
                        since = until + relativedelta(months=-1, day=1)
                        until = since + relativedelta(months=+1)
                        
                        since = int(time.mktime(since.timetuple()))
                        until = int(time.mktime(until.timetuple()))

                    if lap > 2:
                        lap = 0
                        main_loop = False
                        ifp.first_load_weekly = True
                        ifp.save()