# -*- coding: utf-8 -*-

import requests_mock

from tests.api import TestCaseApi
from tests.payload import (
    NETWORK_WIFIDEVICE_PAYLOAD,
    NETWORK_WANSTATUS_PAYLOAD,
    SYSTEM_INFO_PAYLOAD,
)


class TestMesh(TestCaseApi):

    @requests_mock.Mocker()
    def test_network_wifidevice(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=NETWORK_WIFIDEVICE_PAYLOAD,
        )

        devices = self.client.mesh.network_wifidevice()

        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]['hostname'], 'iPad')
        self.assertEqual(devices[1]['mac'], '1a:e6:cf:84:6d:22')

        self.http.sid = None

    @requests_mock.Mocker()
    def test_network_wanstatus(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=NETWORK_WANSTATUS_PAYLOAD,
        )

        wanstatus = self.client.mesh.network_wanstatus()
        self.assertEqual(wanstatus['wan_connected'], True)

        self.http.sid = None

    @requests_mock.Mocker()
    def test_system_info(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=SYSTEM_INFO_PAYLOAD,
        )

        system_info = self.client.mesh.system_info()
        self.assertEqual(
            system_info['nodes'][0]['firmware_ver'],
            'SRM 1.2-7742 Update 5',
        )

        self.http.sid = None
