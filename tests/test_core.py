# -*- coding: utf-8 -*-

import requests_mock

from tests.api import TestCaseApi
from tests.payload import (
    NETWORK_NSM_DEVICE_PAYLOAD,
    SYSTEM_UTILIZATION_PAYLOAD,
    DDNS_EXTIP_PAYLOAD,
    DDNS_RECORD_PAYLOAD,
)


class TestCore(TestCaseApi):

    @requests_mock.Mocker()
    def test_system_utilization(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=SYSTEM_UTILIZATION_PAYLOAD,
        )

        system_utilization = self.client.core.system_utilization()

        self.assertEqual(system_utilization['cpu']['5min_load'], 9)
        self.assertEqual(system_utilization['memory']['avail_swap'], 260332)

        self.http.sid = None

    @requests_mock.Mocker()
    def test_ddns_extip(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=DDNS_EXTIP_PAYLOAD,
        )

        ddns_extip = self.client.core.ddns_extip()

        self.assertEqual(len(ddns_extip), 1)
        self.assertEqual(ddns_extip[0]['ip'], '92.10.197.59')

        self.http.sid = None

    @requests_mock.Mocker()
    def test_ddns_record(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=DDNS_RECORD_PAYLOAD,
        )

        ddns_record = self.client.core.ddns_record()

        self.assertEqual(len(ddns_record['records']), 1)
        self.assertEqual(
            ddns_record['records'][0]['hostname'],
            'foobar.synology.me',
        )

        self.http.sid = None

    @requests_mock.Mocker()
    def test_network_nsm_device(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=NETWORK_NSM_DEVICE_PAYLOAD
        )

        devices = self.client.core.network_nsm_device()

        self.assertEqual(len(devices), 3)
        self.assertEqual(devices[1]['hostname'], 'DiskStation')

        devices = self.client.core.network_nsm_device(True)

        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[1]['hostname'], 'DiskStation')

        devices = self.client.core.network_nsm_device(False)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['hostname'], 'Computer')

        self.http.sid = None
