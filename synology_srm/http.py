# -*- coding: utf-8 -*-

import requests
import urllib3

class Http(object):
    """HTTP connection to the API.

    This class is responsible for handling all communications with the API.
    """

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
        """Disable the HTTPS certificate check.
        This should be used only when using self-signed certificate.
        """
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
        """Perform an HTTP call to the Synology API."""
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

        if response.status_code != 200:
            raise SynologyHttpException(
                "The server answered a wrong status code (code={})".format(
                    response.status_code
                )
            )

        data = response.json()

        if 'success' not in data and (
            'data' not in data or
            'error' not in data
        ):
            raise SynologyHttpException(
                "The output received by the server is malformed"
            )

        if not data['success']:
            code = data['error']['code']
            if code == 400:
                raise SynologyIncorrectPasswordException(
                    400,
                    "No such account or incorrect password"
                )
            if code == 401:
                raise SynologyAccountDisabledException(
                    401,
                    "Account disabled"
                )
            if code == 402:
                raise SynologyPermissionDeniedException(
                    402,
                    "Permission denied"
                )

            raise SynologyException(
                code,
                "Unknown error, please check the Synology API documentation"
            )

        return data['data']

class SynologyException(Exception):
    """Base Synology exception from HTTP requests."""
    def __init__(self, code, message):
        self.code = code
        message = "{} (error={})".format(message, code)
        super(SynologyException, self).__init__(message)

class SynologyHttpException(Exception):
    pass

class SynologyIncorrectPasswordException(SynologyException):
    """API error code 400."""
    pass

class SynologyAccountDisabledException(SynologyException):
    """API error code 401."""
    pass

class SynologyPermissionDeniedException(SynologyException):
    """API error code 402."""
    pass

