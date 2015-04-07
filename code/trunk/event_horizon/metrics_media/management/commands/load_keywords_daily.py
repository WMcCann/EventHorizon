#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys, os
import csv

import time
import datetime

from dateutil.relativedelta import relativedelta
from oauth2client.django_orm import Storage

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from googleads import adwords
from googleads import oauth2

from media.models import AdwordsAccount
from services_media.models import AdwordsConnection
from metrics_media.models import AdwordsKeyword


class Command(BaseCommand):
    args = ''
    help = 'Load keywords'

    def handle(self, *args, **options):
        accs = [a for a in AdwordsAccount.objects.filter(first_load_keyword=True, deleted=False)]
        for acc in accs:
            if acc:
                storage = Storage(AdwordsConnection, 'email', acc.adwords_connection.email, 'credential')
                credential = storage.get()
                if credential is None or credential.invalid == True:
                    CommandError(u'AdwordsConnection is invalid')

                oauth2_client = oauth2.GoogleRefreshTokenClient(
                    settings.ADWORDS_CLIENT_ID, settings.ADWORDS_CLIENT_SECRET, credential.refresh_token)

                client = adwords.AdWordsClient(
                    settings.ADWORDS_DEVELOPER_TOKEN, oauth2_client, 'EventHorizon', acc.client_id)

                customer = client.GetService('CustomerService').get()
                print 'You are logged in as customer: %s' % customer['customerId']
                
                report_downloader = client.GetReportDownloader(version='v201402')

                until = datetime.datetime.today()
                until = until + relativedelta(days=-1)
                since = until

                # Create report definition.
                report = {
                    'reportName': 'Custom Date KEYWORDS_PERFORMANCE_REPORT',
                    'dateRangeType': 'CUSTOM_DATE',
                    'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
                    'downloadFormat': 'CSV',
                    'selector': {
                        'fields': [
                            'Date',
                            'Status', 'Id', 'KeywordText',
                            'CampaignId', 'CampaignName', 'CampaignStatus', 
                            'AdGroupId', 'AdGroupName', 'AdGroupStatus',
                            'PlacementUrl',
                            'MaxCpc', 'Clicks', 'Impressions', 'Cost', 
                            'SearchImpressionShare', 'SearchExactMatchImpressionShare', 'AveragePosition',
                            'Week',
                            ],
                        'dateRange': {
                            'min': since.strftime('%Y%m%d'),
                            'max': until.strftime('%Y%m%d')
                        }
                    },
                    # Enable to get rows with zero impressions.
                    'includeZeroImpressions': 'false'
                    }

                # You can provide a file object to write the output to. For this demonstration
                # we use sys.stdout to write the report to the screen.
                filename = os.path.join(settings.PROJECT_ROOT_PATH, 'public', 'media', 'adwords', '%s_kw_%s.csv' % (acc.client_id, until.strftime('%Y-%m-%d')))

                f = open(filename,'w')
                report_downloader.DownloadReport(report, f)
                f.close()

                bulk = []
                with open(filename, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for i, row in enumerate(spamreader):
                        if i > 1 and not row[0] == 'Total':
                            bulk.append(
                                AdwordsKeyword(
                                    adwords_account=acc,
                                    day=datetime.datetime.strptime(row[0], '%Y-%m-%d'),
                                    keyword_status=row[1],
                                    keyword_id=row[2],
                                    keyword=row[3],
                                    campaign_status=row[6],
                                    campaign_id=row[4],
                                    campaign=row[5],
                                    adgroup_status=row[9],
                                    adgroup_id=row[7],
                                    adgroup=row[8],
                                    placement_url=row[10],
                                    max_cpc=int(row[11]),
                                    clicks=int(row[12]),
                                    impressions=int(row[13]),
                                    cost=int(row[14]),
                                    search_impressions_share=row[15],
                                    search_exact_match=row[16],
                                    avg_position=float(row[17]),
                                    week=datetime.datetime.strptime(row[18], '%Y-%m-%d'),
                                    )
                                )

                AdwordsKeyword.objects.bulk_create(bulk)