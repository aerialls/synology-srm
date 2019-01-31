# -*- coding: utf-8 -*-

import unittest
import synology_srm


class TestBase(unittest.TestCase):
    def setUp(self):
        """Set up things to be run when tests are started."""
        self.client = synology_srm.Client(
            host='192.168.1.254',
            port=8001,
            username='admin',
            password='admin',
        )

        self.http = self.client.http

    def _mock_login(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'sid': 'secret_sid'
            },
            'success': True
        })
