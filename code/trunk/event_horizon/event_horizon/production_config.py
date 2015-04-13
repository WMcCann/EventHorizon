#!/usr/bin/python
# -*- coding: utf-8 -*-


# Facebook Event Horizon App
FB_CLIENT_ID = '1377187942506962'
FB_CLIENT_SECRET = '870fc0f8f694cb2b2ebbaf458abaa88d'
FB_REDIRECT_URI = 'http://splzzz96.la.corp.ipgnetwork.com/services/social/facebook-connection/oauth/'
FB_SCOPE = ['read_insights', 'manage_pages']


# Twitter Event Horizon App
TW_CONSUMER_KEY = 'Ugl2MGLJiOz8tbtr7u3zhw'
TW_CONSUMER_SECRET = 'EK5RzPGVjeLFGDw04zvxfS6kc1NuHyvJHMD8Um0'
TW_REDIRECT_URI = 'http://splzzz96.la.corp.ipgnetwork.com/services/social/twitter-connection/oauth/'


# Youtube Event Horizon App
YT_REDIRECT_URI = 'http://splzzz96.la.corp.ipgnetwork.com/services/social/youtube-connection/oauth/'
YT_ANALYTICS_REDIRECT_URI = 'http://splzzz97.la.corp.ipgnetwork.com/social/analytics/youtube-channel/oauth/'


# Adwords Event Horizon App
ADWORDS_DEVELOPER_TOKEN = 'KNY7B1mYuCX7CqUXAzxmiQ'
ADWORDS_CLIENT_ID = '17825692816-9rctugnmfadq5bi10rikebk90d8qlrdc.apps.googleusercontent.com'
ADWORDS_CLIENT_SECRET = 'AezResEiY8u8_DTpd7uCmoe5'
ADWORDS_REDIRECT_URI = 'http://splzzz96.la.corp.ipgnetwork.com/services/media/adwords-connection/oauth/'



DATABASES = {
    'default': {
        'ENGINE': 'sqlserver_ado', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'EVENTHORIZON_DEV',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'eventhorizon',
        'PASSWORD': 'Wmccann01',
        'HOST': '10.226.0.95',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
        'TEST_CREATE': False,
        'OPTIONS': {
            'provider': 'SQLOLEDB',
            'use_mars': True,
        },
    }
}