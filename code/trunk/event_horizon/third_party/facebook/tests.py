# coding: utf-8

import mock
import unittest

from .facebook import FacebookClient


class FacebookClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = FacebookClient()

    def test_client_initialize_with_version_2(self):
        self.assertEqual('v2.0', self.client._version)

    def test_create_url_generate_url_with_version_2(self):
        url = self.client._create_url('/me')
        expected_url = 'https://graph.facebook.com/v2.0/me?'
        self.assertEqual(expected_url, url)

    def test_oauth_url_generate_version_2_url(self):
        url = self.client.oauth_url(redirect_uri='', scope=[])
        expected_url = 'https://graph.facebook.com/v2.0/oauth/authorize?scope=&redirect_uri=&client_id=None&popup=true'
        self.assertEqual(expected_url, url)

    def test_make_path_returns_version_2_path(self):
        path = '/oauth'
        expected_path = '/v2.0/oauth'
        self.assertEqual(expected_path, self.client._make_path(path))

    @mock.patch.object(FacebookClient, '_get')
    def test_short_lived_token_calls_version_2(self, get_mock):
        get_mock.return_value = 'access_token=123123123&expires=123'
        token, _ = self.client.short_lived_token(None, None)
        self.assertTrue(get_mock.called)

        args, kwargs = get_mock.call_args
        url = args[0]

        self.assertEqual('/v2.0/oauth/access_token', url)
        self.assertEqual(token, '123123123')

    @mock.patch.object(FacebookClient, '_get')
    def test_long_lived_token_calls_version_2(self, get_mock):
        get_mock.return_value = 'access_token=123123123&expires=123'
        token, _ = self.client.long_lived_token('123')

        args, kwargs = get_mock.call_args
        called_url = args[0]
        expected_url = '/v2.0/oauth/access_token'

        self.assertEqual(expected_url, called_url)
        self.assertEqual(token, '123123123')

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_me_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = None
        get_mock.return_value = None

        self.client.me()

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/me'

        self.assertEqual(expected_url, called_url)

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_accounts_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = None
        get_mock.return_value = None

        self.client.accounts('123')

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/123/accounts'

        self.assertEqual(expected_url, called_url)

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_insights_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = {}
        get_mock.return_value = None

        self.client.insights('123', 'test_metric')

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/123/insights/test_metric'

        self.assertEqual(expected_url, called_url)

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_insights_with_period_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = {}
        get_mock.return_value = None

        self.client.insights('123', 'test_metric', 'test_period')

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/123/insights/test_metric/test_period'

        self.assertEqual(expected_url, called_url)

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_feed_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = {}
        get_mock.return_value = None

        self.client.feed('123')

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/123/feed'

        self.assertEqual(expected_url, called_url)

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_likes_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = {}
        get_mock.return_value = None

        self.client.likes('123')

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/123/likes'

        self.assertEqual(expected_url, called_url)

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_comments_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = {}
        get_mock.return_value = None

        self.client.comments('123')

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/123/comments'

        self.assertEqual(expected_url, called_url)

    @mock.patch.object(FacebookClient, '_get')
    @mock.patch.object(FacebookClient, '_get_auth_params')
    def test_obj_id_calls_version_2(self, auth_mock, get_mock):
        auth_mock.return_value = {}
        get_mock.return_value = None

        self.client.obj_id('123123')

        args = get_mock.call_args[0]
        called_url = args[0]
        expected_url = '/v2.0/123123'

        self.assertEqual(expected_url, called_url)

    def test_get_auth_params_raises_exception_when_token_is_empty(self):
        with self.assertRaises(Exception):
            self.client._get_auth_params()

    def test_get_auth_params_return_access_token(self):
        self.client._access_token = 123
        auth_params = self.client._get_auth_params()

        self.assertEqual({'access_token': 123}, auth_params)
