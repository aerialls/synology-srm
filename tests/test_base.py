# -*- coding: utf-8 -*-

import requests_mock

from tests.api import TestCaseApi


class TestBase(TestCaseApi):

    @requests_mock.Mocker()
    def test_info(self, m):
        self._mock_login(m)
        m.get('{}/query.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'SYNO.API.Auth': {
                    'maxVersion': 3,
                    'minVersion': 1,
                    'path': 'auth.cgi'
                },
                'SYNO.API.Encryption': {
                    'maxVersion': 1,
                    'minVersion': 1,
                    'path': 'encryption.cgi'
                },
            },
            'success': True
        })

        info = self.client.base.info()

        self.assertEqual(len(info), 2)
        self.assertEqual(info['SYNO.API.Auth']['path'], 'auth.cgi')

        self.http.sid = None

    @requests_mock.Mocker()
    def test_encryption(self, m):
        self._mock_login(m)
        m.get('{}/encryption.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'cipherkey': '__cIpHeRtExT',
                'ciphertoken': '__cIpHeRtOkEn',
                'public_key': 'MIICIjAePcdf3xkxu9bN3odke8BREE3+AC8x00RJr1WI3NVTLThCRBexrsQXbqL8We8Jy0g9UfM92zTgMW05sG0YLifpXwBwMEK6c3c07Yyp3qi+mMvr5mhVhSgK0cEOw3rzOYlsrY0ritziADWNbYY37DcfusyKYKMyLjcat9AYs1NDGBW2aWuUQRQzbd/jAcrqb3+xXN0dJKnpk8EiBiM7srBzMynVaf4nftQO9gtuErefiLXIjjNTy/PQwUeja1gXhonEiQ3HIOdwXwosfmwUZAomn2Oy87ThXYUILvzUfNI8rzGlyOqrQMsQ3sRPUn7Xg03nJQH9IcoU6M6v35ABjrSJHrtcvVThnYg/Ht2WxNYWi9YvUu5kuSfQK1d0qtKk/Wic0inTs5xHjks+wx5NaLxbrUR/uFB+M+en5UmxzLCDcmqWaKlUHhCAduM4NBnC5IVTCjvmL5De/ohIZzLSmvpO9jr4ql/G7eIOwMy2gAu1Tkl0FunkOCrVmtIA7irmV1cVi80eSIKefEMroerPXULiTUV9ESTz/UtBewuZrmrfpE/ki9XpExiZYum4MRa5tsAHl+on9Z3z9fxHrafKYvlv1WBY0Oq4qdxBV6VX0KCX74oq7qYq2Vzm7Mg2xTgxWZmnfZK/xoyd/msx3vv6MCAwEAAQ==',  # noqa: E501
                'server_time': 1550255617
            },
            'success': True
        })

        encryption = self.client.base.encryption()

        self.assertEqual(encryption['cipherkey'], '__cIpHeRtExT')

        self.http.sid = None
