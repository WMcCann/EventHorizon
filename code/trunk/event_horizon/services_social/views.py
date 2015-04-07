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

from third_party.facebook.facebook import FacebookClient

from services_social.models import FacebookConnection, TwitterConnection, YoutubeConnection


def facebook_connection_add(request):

    """
    View to redirect the user to Facebook auth page.

    URI: /services/social/facebook-connection/add/

    """

    client = FacebookClient(
        client_id=settings.FB_CLIENT_ID, 
        client_secret=settings.FB_CLIENT_SECRET,
        )

    return redirect(client.oauth_url(settings.FB_REDIRECT_URI, settings.FB_SCOPE))


def facebook_connection_oauth(request):

    """
    View to request long lived token and save it in our base.
    It'll return 404 if 'code' param doesn't exist.

    URI: /services/social/facebook-connection/oauth/

    """

    code = request.GET.get('code', None)
    if code:
        client = FacebookClient(
            client_id=settings.FB_CLIENT_ID, 
            client_secret=settings.FB_CLIENT_SECRET,
            )

        sl_token, sl_expires = client.short_lived_token(settings.FB_REDIRECT_URI, code)
        ll_token, ll_expires = client.long_lived_token(sl_token)

        client._access_token = ll_token

        me = client.me()

        fbc, created = FacebookConnection.objects.get_or_create(
            conn_id=me['id'],
            deleted=False,
            defaults={
                'name': me['name'],
                'access_token': ll_token,
                'expires': ll_expires,
                }
            )

        if not created:
            fbc.name = me['name']
            fbc.access_token = ll_token
            fbc.expires = ll_expires

        fbc.save()
        return redirect('/admin/services_social/facebookconnection/')
    else:
        raise Http404


def twitter_connection_add(request):

    """
    View to redirect the user to Twitter auth page.

    URI: /services/social/twitter-connection/add/

    """

    auth = tweepy.OAuthHandler(
        settings.TW_CONSUMER_KEY, 
        settings.TW_CONSUMER_SECRET,
        )

    redirect_uri = auth.get_authorization_url()

    request.session['request_token'] = (
        auth.request_token.key, 
        auth.request_token.secret,
        )

    return redirect(redirect_uri)


def twitter_connection_oauth(request):

    """
    View to request token and save it in our base.
    It'll return 404 if token doesn't exist.

    URI: /services/social/twitter-connection/oauth/

    """

    token = request.session.get('request_token')
    del request.session['request_token']

    oauth_token = request.GET.get('oauth_token', None)
    oauth_verifier = request.GET.get('oauth_verifier', None)

    if oauth_token and oauth_verifier:
        auth = tweepy.OAuthHandler(
            settings.TW_CONSUMER_KEY, 
            settings.TW_CONSUMER_SECRET,
            )

        auth.set_request_token(token[0], token[1])
        auth.get_access_token(oauth_verifier)

        api = tweepy.API(auth)
        twc, created = TwitterConnection.objects.get_or_create(
            name=api.me().name,
            deleted=False,
            defaults={
                'access_token': auth.access_token.key,
                'access_token_secret': auth.access_token.secret,
                }
            )

        if not created:
            twc.name = api.me().screen_name
            twc.access_token = auth.access_token.key
            twc.expires = auth.access_token.secret

        twc.save()
        return redirect('/admin/services_social/twitterconnection/')
    else:
        raise Http404


def youtube_connection_add(request):

    """
    View to redirect the user to Youtube auth page.

    URI: /services/social/youtube-connection/add/

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
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email',
                ],
            redirect_uri=settings.YT_REDIRECT_URI,
            access_type='offline', # This is the default
            approval_prompt='force',
            )

    return redirect(flow.step1_get_authorize_url())


def youtube_connection_oauth(request):

    """
    View to request token and save it in our base.
    It'll return 404 if token doesn't exist.

    URI: /services/social/youtube-connection/oauth/

    """
    code = request.GET.get('code', None)
    if code:
        filename = os.path.join(settings.PROJECT_ROOT_PATH, 'event_horizon', 'client_secrets.json')
        flow = flow_from_clientsecrets(
            filename,
            scope=[
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email',
                ],
            redirect_uri=settings.YT_REDIRECT_URI,
            )

        credentials = flow.step2_exchange(code)

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = build('oauth2', 'v2', http=http)

        user_info = service.userinfo().get().execute()

        storage = Storage(YoutubeConnection, 'email', user_info[u'email'], 'credential')
        credential = storage.get()
        if credential is None or credential.invalid == True:
            storage = Storage(YoutubeConnection, 'email', user_info[u'email'], 'credential')
            storage.put(credentials)
        
        return redirect('/admin/services_social/youtubeconnection/')
    else:
        raise Http404

