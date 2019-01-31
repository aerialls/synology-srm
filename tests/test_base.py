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
