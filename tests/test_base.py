# -*- coding: utf-8 -*-

import requests_mock

from tests.api import TestCaseApi
from tests.payload import (
    INFO_PAYLOAD,
    ENCRYPTION_PAYLOAD,
)


class TestBase(TestCaseApi):

    @requests_mock.Mocker()
    def test_info(self, m):
        self._mock_login(m)
        m.get(
            '{}/query.cgi'.format(self.http._get_base_url()),
            json=INFO_PAYLOAD,
        )

        info = self.client.base.info()

        self.assertEqual(len(info), 2)
        self.assertEqual(info['SYNO.API.Auth']['path'], 'auth.cgi')

        self.http.sid = None

    @requests_mock.Mocker()
    def test_encryption(self, m):
        self._mock_login(m)
        m.get(
            '{}/encryption.cgi'.format(self.http._get_base_url()),
            json=ENCRYPTION_PAYLOAD,
        )

        encryption = self.client.base.encryption()

        self.assertEqual(encryption['cipherkey'], '__cIpHeRtExT')

        self.http.sid = None
