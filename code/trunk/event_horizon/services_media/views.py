#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import httplib2
import tweepy
import json

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.django_orm import Storage
from apiclient.discovery import build

from services_media.models import AdwordsConnection


def adwords_connection_add(request):

    """
    View to redirect the user to Adwords auth page.

    URI: /services/media/adwords-connection/add/

    """
    # load file
    filename = os.path.join(settings.PROJECT_ROOT_PATH, 'event_horizon', 'client_secrets.json')
    client_secrets = []
    with open(filename) as f:
        for line in f:
            client_secrets.append(json.loads(line))

    flow = OAuth2WebServerFlow(
            client_id=client_secrets[0][u'web'][u'client_id'],
            client_secret=client_secrets[0][u'web'][u'client_secret'],
            scope=[
                'https://adwords.google.com/api/adwords/',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email',
                ],
            redirect_uri=settings.ADWORDS_REDIRECT_URI,
            access_type='offline', # This is the default
            approval_prompt='force',
            )

    return redirect(flow.step1_get_authorize_url())


def adwords_connection_oauth(request):

    """
    View to request token and save it in our base.
    It'll return 404 if token doesn't exist.

    URI: /services/media/adwords-connection/oauth/

    """
    code = request.GET.get('code', None)
    if code:
        filename = os.path.join(settings.PROJECT_ROOT_PATH, 'event_horizon', 'client_secrets.json')
        flow = flow_from_clientsecrets(
            filename,
            scope=[
                'https://adwords.google.com/api/adwords/',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email',
                ],
            redirect_uri=settings.ADWORDS_REDIRECT_URI,
            )

        credentials = flow.step2_exchange(code)

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = build('oauth2', 'v2', http=http)

        user_info = service.userinfo().get().execute()

        storage = Storage(AdwordsConnection, 'email', user_info[u'email'], 'credential')
        credential = storage.get()
        if credential is None or credential.invalid == True:
            storage = Storage(AdwordsConnection, 'email', user_info[u'email'], 'credential')
            storage.put(credentials)
        
        return redirect('/admin/services_media/adwordsconnection/')
    else:
        raise Http404

