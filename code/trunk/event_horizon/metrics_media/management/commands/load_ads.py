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
from metrics_media.models import AdwordsKeyword, AdwordsAd


class Command(BaseCommand):
    args = ''
    help = 'Load keywords'

    def handle(self, *args, **options):
        accs = [a for a in AdwordsAccount.objects.filter(first_load_ad=False, deleted=False)]
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
                since = until + relativedelta(days=-until.day)
                since = since + relativedelta(months=-3, day=1)

                # Create report definition.
                report = {
                    'reportName': 'Custom Date KEYWORDS_PERFORMANCE_REPORT',
                    'dateRangeType': 'CUSTOM_DATE',
                    'reportType': 'AD_PERFORMANCE_REPORT',
                    'downloadFormat': 'CSV',
                    'selector': {
                        'fields': [
                            'Date',
                            'Status', 'Id', 'PromotionLine',
                            'Description1', 'Description2',
                            'DisplayUrl',
                            'Url',
                            'CampaignId', 'CampaignName', 'CampaignStatus', 
                            'AdGroupId', 'AdGroupName', 'AdGroupStatus',
                            'Clicks', 'Impressions', 'Cost', 
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
                filename = os.path.join(settings.PROJECT_ROOT_PATH, 'public', 'media', 'adwords', '%s_ad_initial.csv' % acc.client_id)

                f = open(filename,'w')
                report_downloader.DownloadReport(report, f)
                f.close()

                bulk = []
                with open(filename, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for i, row in enumerate(spamreader):
                        if i > 1 and not row[0] == 'Total':
                            bulk.append(
                                AdwordsAd(
                                    adwords_account=acc,
                                    day=datetime.datetime.strptime(row[0], '%Y-%m-%d'),
                                    ad_status=row[1],
                                    ad_id=row[2],
                                    ad=row[3],
                                    description_1=row[4],
                                    description_2=row[5],
                                    display_url=row[6],
                                    url=row[7],
                                    campaign_status=row[10],
                                    campaign_id=row[8],
                                    campaign=row[9],
                                    adgroup_id=row[11],
                                    adgroup=row[12],
                                    adgroup_status=[13],
                                    clicks=int(row[14]),
                                    impressions=int(row[15]),
                                    cost=int(row[16]),
                                    )
                                )

                AdwordsAd.objects.bulk_create(bulk)
                acc.first_load_ad = True
                acc.save()