# -*- coding: utf-8 -*-

import requests_mock

from tests.api import TestCaseApi
from synology_srm.http import (
    SynologyHttpException,
    SynologyAccountDisabledException,
    SynologyIncorrectPasswordException,
    SynologyPermissionDeniedException
)


class TestLogin(TestCaseApi):

    def test_initial_state(self):
        self.assertIs(self.client.http.sid, None)

    @requests_mock.Mocker()
    def test_not_found_error(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), status_code=404)

        with self.assertRaises(SynologyHttpException):
            self.http._login()

    @requests_mock.Mocker()
    def test_wrong_output(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'hello': 'world'
        })

        with self.assertRaises(SynologyHttpException):
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
    def test_refresh_sid_login(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), [
            {
                'json': {
                    'data': {
                        'sid': 'sid_one'
                    },
                    'success': True
                }
            },
            {
                'json': {
                    'data': {
                        'sid': 'sid_two'
                    },
                    'success': True
                }
            }
        ])

        m.get('{}/entry.cgi'.format(self.http._get_base_url()), [
            {
                'json': {
                    'error': {
                        'code': 106
                    },
                    'success': False
                }
            },
            {
                'json': {
                    'data': {
                         'devices': []
                    },
                    'success': True
                }
            }
        ])

        self.http._login()
        self.assertEqual(self.http.sid, 'sid_one')

        # Try another API to force the SID renewal
        devices = self.client.mesh.network_wifidevice()

        self.assertEqual(self.http.sid, 'sid_two')
        self.assertEqual(devices, [])

    @requests_mock.Mocker()
    def test_loop_redirect(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'sid': 'sid'
            },
            'success': True
        })

        m.get('{}/entry.cgi'.format(self.http._get_base_url()), [
            {
                'json': {
                    'error': {
                        'code': 106
                    },
                    'success': False
                }
            },
            {
                'json': {
                    'error': {
                        'code': 106
                    },
                    'success': False
                }
            }
        ])

        with self.assertRaises(SynologyHttpException):
            self.client.mesh.network_wifidevice()

    @requests_mock.Mocker()
    def test_login_or_password_incorrect(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'error': {
                'code': 400
            },
            'success': False
        })

        with self.assertRaises(SynologyIncorrectPasswordException):
            self.http._login()

    @requests_mock.Mocker()
    def test_account_disabled(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'error': {
                'code': 401
            },
            'success': False
        })

        with self.assertRaises(SynologyAccountDisabledException):
            self.http._login()

    @requests_mock.Mocker()
    def test_permission_denied(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'error': {
                'code': 402
            },
            'success': False
        })

        with self.assertRaises(SynologyPermissionDeniedException):
            self.http._login()
