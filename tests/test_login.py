# -*- coding: utf-8 -*-

import unittest
import requests_mock
import synology_srm

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Set up things to be run when tests are started."""
        self.client = synology_srm.Client(
            host='192.168.1.254',
            port=8001,
            username='admin',
            password='admin'
        )

        self.http = self.client.http

    def test_initial_state(self):
        self.assertIs(self.client.http.sid, None)

    @requests_mock.Mocker()
    def test_not_found_error(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), status_code=404)

        with self.assertRaises(synology_srm.SynologyHttpException) as cm:
            self.http._login()

    @requests_mock.Mocker()
    def test_wrong_output(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'hello': 'world'
        })

        with self.assertRaises(synology_srm.SynologyHttpException) as cm:
            self.http._login()

    @requests_mock.Mocker()
    def test_successful_login(self, m):
        sid = 'Sylgv43ED9AAECBBFD5C08D1D'
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'sid': sid
            },
            'success': True
        })

        self.http._login()
        self.assertEqual(self.http.sid, sid)
        self.http.sid = None

    @requests_mock.Mocker()
    def test_login_or_password_incorrect(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'error': {
                'code': 400
            },
            'success': False
        })

        with self.assertRaises(synology_srm.SynologyIncorrectPasswordException) as cm:
            self.http._login()

    @requests_mock.Mocker()
    def test_account_disabled(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'error': {
                'code': 401
            },
            'success': False
        })

        with self.assertRaises(synology_srm.SynologyAccountDisabledException) as cm:
            self.http._login()

    @requests_mock.Mocker()
    def test_permission_denied(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'error': {
                'code': 402
            },
            'success': False
        })

        with self.assertRaises(synology_srm.SynologyPermissionDeniedException) as cm:
            self.http._login()
