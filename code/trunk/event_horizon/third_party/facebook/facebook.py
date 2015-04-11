#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
import json
import urlparse
import time
import datetime
import logging

from urllib import urlencode

from tornado import httpclient, ioloop, gen

from .exceptions import FacebookGenericError


class FacebookClient(object):

    """
    FacebookClient
    =========

    FacebookClient is a client for Facebook API.

    """

    def __init__(self, client_id=None, client_secret=None, access_token=None):
        self.client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token

        self._endpoint = 'graph.facebook.com'
        self._protocol = 'https'
        self._conn = httplib.HTTPSConnection(self._endpoint)

        self.async_queue = set()
        self.async_http_client = httpclient.AsyncHTTPClient()
        self.tasks = {}

        self._version = 'v2.0'

    def start_async_tasks(self, tasks, **kwargs):
        self.tasks = tasks
        for task in tasks:
            self.async_get(task, **kwargs)

        if tasks:
            ioloop.IOLoop.instance().start()

    @gen.engine
    def async_get(self, task, **kwargs):
        _id = task.get(u'id')

        print(u'Processing task: %s' % _id)

        params = self._get_auth_params()
        params.update(task.get(u'kwargs'))

        path = task.get(u'path')
        self.async_queue.add(path)

        url = self._create_url(path, **params)

        try:
            response = yield gen.Task(self.async_http_client.fetch, url)
        except Exception:
            task[u'response'] = None
        else:
            if response.error:
                logging.error(response.error)
            else:
                print(u'Getting %s' % _id)
                task[u'response'] = json.loads(response.body)

        self.async_queue.remove(path)
        if not self.async_queue:
            ioloop.IOLoop.instance().stop()

    def _make_path(self, path):
        return '/{version}{path}'.format(version=self._version, path=path)

    def _create_url(self, path, **kwargs):
        url = '{protocol}://{endpoint}{path}?{querystring}'.format(
            protocol=self._protocol, endpoint=self._endpoint,
            path=self._make_path(path), querystring=urlencode(kwargs)
        )

        return url

    def _get_auth_params(self):
        if self._access_token:
            return {'access_token': self._access_token}
        else:
            raise Exception(u'You need to authorize.')

    def _join(self, array=[]):
        array = [str(a) for a in array]
        return ','.join(array)

    def _get(self, url, params=None, json_response=True):
        response = u''

        if params:
            params = urlencode(params)
            url = url + '?' + params
        times = 0

        while True:
            try:
                self._conn.request('GET', url)
                response = self._conn.getresponse()

                if not json_response:
                    return response.read()

                data = json.loads(response.read())
                if u'error' in data:
                    raise FacebookGenericError(data['error'])
                return data

            except httplib.BadStatusLine, e:
                self._conn.close()
                self._conn.connect()

                times += 1
                if times < 3:
                    continue
                else:
                    raise e
            except (ValueError, TypeError):
                # empty response
                return None

    def _post(self, url, body=None, params=None, json_response=True):
        if body:
            body = urlencode(body)
        if params:
            params = urlencode(params)
            url = url + '?' + params
        times = 0
        while True:
            try:
                self._conn.request('POST', url, body, {'Content-type': 'application/x-www-form-urlencoded'})
                response = self._conn.getresponse()

                if not json_response:
                    return response.read()

                data = json.loads(response.read())
                if u'error' in data:
                    raise FacebookGenericError(data['error'])
                return data

            except httplib.BadStatusLine, e:
                self._conn.close()
                self._conn.connect()

                times += 1
                if times < 3:
                    continue
                else:
                    raise e
            except (ValueError, TypeError):
                # empty response
                return None

    def oauth_url(self, redirect_uri, scope):
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': self._join(scope),
            'popup': 'true',
            }

        url = self._create_url('/oauth/authorize', **params)
        return url

    def short_lived_token(self, redirect_uri, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self._client_secret,
            'redirect_uri': redirect_uri,
            'code': code,
            }

        url = self._make_path('/oauth/access_token')

        data = self._get(url, params, json_response=False)
        qs = urlparse.parse_qs(data)
        return qs['access_token'][0], datetime.datetime.fromtimestamp(time.time() + int(qs['expires'][0]))

    def long_lived_token(self, short_lived_token):
        params = {
            'client_id': self.client_id,
            'client_secret': self._client_secret,
            'grant_type': 'fb_exchange_token',
            'fb_exchange_token': short_lived_token,
            }

        url = self._make_path('/oauth/access_token')

        data = self._get(url, params, json_response=False)
        qs = urlparse.parse_qs(data)
        return qs['access_token'][0], datetime.datetime.fromtimestamp(time.time() + int(qs['expires'][0]))

    def me(self):
        params = self._get_auth_params()

        url = self._make_path('/me')
        data = self._get(url, params)
        return data

    def accounts(self, user_id):
        params = self._get_auth_params()
        url = self._make_path('/%s/accounts' % str(user_id))
        data = self._get(url, params)
        return data

    def insights(self, insights_id, metric, period=None, **kwargs):
        params = self._get_auth_params()
        params.update(kwargs)
        if period:
            url = '/%s/insights/%s/%s' % (str(insights_id), metric, period)
        else:
            url = '/%s/insights/%s' % (str(insights_id), metric)
        data = self._get(self._make_path(url), params)
        return data

    def feed(self, obj_id, **kwargs):
        params = self._get_auth_params()
        params.update(kwargs)
        url = self._make_path('/%s/feed' % str(obj_id))
        data = self._get(url, params)
        return data

    def likes(self, obj_id, **kwargs):
        params = self._get_auth_params()
        params.update(kwargs)
        url = self._make_path('/%s/likes' % str(obj_id))
        data = self._get(url, params)
        return data

    def comments(self, obj_id, **kwargs):
        params = self._get_auth_params()
        params.update(kwargs)
        url = self._make_path('/%s/comments' % str(obj_id))
        data = self._get(url, params)
        return data

    def obj_id(self, obj_id, **kwargs):
        params = self._get_auth_params()
        params.update(kwargs)
        url = self._make_path('/%s' % str(obj_id))
        data = self._get(url, params)
        return data
