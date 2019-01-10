# -*- coding: utf-8 -*-

import requests
import urllib3

class SynologyHttpException(Exception):
    pass

class Http(object):

    def __init__(self, host: str, port: int,
        username: str, password: str, https: bool = True):
        self.host = host
        self.port = port

        self.username = username
        self.password = password

        self.https = https
        self.verify = True

        self.sid = None

    def disable_https_verify(self):
        urllib3.disable_warnings()
        self.verify = False

    def _get_base_url(self):
        return '{}://{}:{}/webapi'.format(
            'https' if self.https else 'http',
            self.host,
            self.port
        )

    def _login(self):
        params = {
            'format': 'sid',
            'account': self.username,
            'passwd': self.password
        }

        response = self.call(
            path='auth.cgi',
            api='SYNO.API.Auth',
            method='Login',
            version=2,
            params=params,
            authorized=False
        )

        self.sid = response['sid']

    def call(self, path: str, api: str, method: str,
        version: int = 1, params: dict = {},
        authorized: bool = True):
        url = '{}/{}'.format(
            self._get_base_url(),
            path
        )

        if authorized and self.sid is None:
            self._login()
            params['_sid'] = self.sid

        params['api'] = api
        params['method'] = method
        params['version'] = version

        response = requests.get(url, verify=self.verify, params=params)
        data = response.json()

        if not data['success']:
            raise SynologyHttpException(
                "The API request on {} was not successful (error={})".format(
                    url,
                    data['error']['code']
            ))

        return data['data']

