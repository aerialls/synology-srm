# -*- coding: utf-8 -*-

import os
import requests
from urllib.parse import urlencode

from requests.packages.urllib3.exceptions import InsecureRequestWarning

COMMON_ERROR_CODES = {
    100: "Unknown error",
    101: "No parameter of API, method or version",
    102: "The requested API does not exist",
    103: "The requested method does not exist",
    104: "The requested version does not support the functionality",
    105: "The logged in session does not have permission",
    106: "Session timeout",
    107: "Session interrupted by duplicate login",
    117: "Need manager rights for operation",
}


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
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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

        errors = {
            400: "No such account or incorrect password",
            401: "Account disabled",
            402: "Permission denied",
            403: "2-step verification code required",
            404: "Failed to authenticate 2-step verification code",
        }

        response = self.call(
            endpoint='auth.cgi',
            api='SYNO.API.Auth',
            method='Login',
            version=2,
            params=params,
            restricted=False,
            errors=errors,
        )

        self.sid = response['sid']

    def _to_query_string(self, params):
        return urlencode(params, doseq=True).replace('+', '%20')

    def download(self, path, **kwargs):
        """Download a file to the local filesystem from the Synology API."""
        request = self.call(stream=True, **kwargs)
        with open(path, 'wb') as stream:
            for chunk in request:
                stream.write(chunk)

    def call(self, endpoint: str, api: str, method: str,
             version: int = 1, params: dict = {}, stream: bool = False,
             restricted: bool = True, retried: bool = False,
             errors: dict = {}):
        """Performs an HTTP call to the Synology API."""
        url = '{}/{}'.format(
            self._get_base_url(),
            endpoint,
        )

        if restricted and self.sid is None:
            self._login()

        cookies = {}
        if self.sid is not None:
            cookies['id'] = self.sid

        params['api'] = api
        params['method'] = method
        params['version'] = version

        response = requests.get(
            url,
            verify=self.verify,
            params=self._to_query_string(params),
            cookies=cookies,
            stream=stream,
        )

        if response.status_code != 200:
            raise SynologyHttpException(
                "The server answered a wrong status code (code={})".format(
                    response.status_code
                )
            )

        if ('content-type' in response.headers and
            response.headers['content-type'] == 'application/zip'
        ):
            return response

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

            if code >= 100 and code < 200:
                message = self._get_common_error_message(code)

                # 106 Session timeout
                # 107 Session interrupted by duplicate login
                if code == 106 or code == 107:
                    if not restricted or retried:
                        # We should stop here if:
                        #  1 - Public route, no need to retry the login
                        #  2 - We already retried the route
                        raise SynologyCommonError(
                            code,
                            message,
                        )
                    self._login()
                    # Retry the current request with a new token
                    return self.call(
                        endpoint=endpoint,
                        api=api,
                        method=method,
                        version=version,
                        params=params,
                        restricted=True,
                        retried=True,
                        errors=errors,
                    )

                raise SynologyCommonError(
                    code,
                    message,
                )

            if code in errors:
                message = errors[code]
            else:
                message = "Unknown API error, please check the documentation"

            raise SynologyApiError(
                code,
                message,
            )

        return data['data']

    def _get_common_error_message(self, code):
        """Gets the official message errror from
        the API documentation
        """
        if code not in COMMON_ERROR_CODES:
            return "Unknown common error, please check the documentation"
        return COMMON_ERROR_CODES[code]


class SynologyException(Exception):
    """Base Synology exception."""
    pass


class SynologyHttpException(SynologyException):
    """Synology HTTP exception."""
    pass


class SynologyError(SynologyException):
    """Base Synology error."""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super(SynologyError, self).__init__(
            "{} (error={})".format(message, code)
        )


class SynologyCommonError(SynologyError):
    """Synology common errror."""
    pass


class SynologyApiError(SynologyError):
    """Synology API error."""
    pass
