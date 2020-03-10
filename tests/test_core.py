# -*- coding: utf-8 -*-

import requests_mock

from tests.api import TestCaseApi
from tests.payload import (
    NETWORK_NSM_DEVICE_PAYLOAD,
    SYSTEM_UTILIZATION_PAYLOAD,
    DDNS_EXTIP_PAYLOAD,
    DDNS_RECORD_PAYLOAD,
    NETWORK_NGFW_TRAFFIC_PAYLOAD,
)


class TestCore(TestCaseApi):

    @requests_mock.Mocker()
    def test_get_system_utilization(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=SYSTEM_UTILIZATION_PAYLOAD,
        )

        system_utilization = self.client.core.get_system_utilization()

        self.assertEqual(system_utilization['cpu']['5min_load'], 9)
        self.assertEqual(system_utilization['memory']['avail_swap'], 260332)

        self.http.sid = None

    @requests_mock.Mocker()
    def test_list_ddns_extip(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=DDNS_EXTIP_PAYLOAD,
        )

        ddns_extip = self.client.core.list_ddns_extip()

        self.assertEqual(len(ddns_extip), 1)
        self.assertEqual(ddns_extip[0]['ip'], '92.10.197.59')

        self.http.sid = None

    @requests_mock.Mocker()
    def test_list_ddns_record(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=DDNS_RECORD_PAYLOAD,
        )

        ddns_record = self.client.core.list_ddns_record()

        self.assertEqual(len(ddns_record['records']), 1)
        self.assertEqual(
            ddns_record['records'][0]['hostname'],
            'foobar.synology.me',
        )

        self.http.sid = None

    @requests_mock.Mocker()
    def test_get_network_nsm_device(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=NETWORK_NSM_DEVICE_PAYLOAD,
        )

        devices = self.client.core.get_network_nsm_device()

        self.assertEqual(len(devices), 3)
        self.assertEqual(devices[1]['hostname'], 'DiskStation')

        devices = self.client.core.get_network_nsm_device({'is_online': True})

        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[1]['hostname'], 'DiskStation')

        devices = self.client.core.get_network_nsm_device({'is_online': False})

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['hostname'], 'Computer')

        devices = self.client.core.get_network_nsm_device({
            'is_online': True,
            'connection': 'ethernet',
        })

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['hostname'], 'DiskStation')

        devices = self.client.core.get_network_nsm_device({
            'is_online': False,
            'connection': 'wifi',
        })

        self.assertEqual(len(devices), 0)

        self.http.sid = None

    @requests_mock.Mocker()
    def test_get_ngfw_traffic(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=NETWORK_NGFW_TRAFFIC_PAYLOAD,
        )

        devices = self.client.core.get_ngfw_traffic(interval='live')

        self.assertEqual(len(devices), 3)
        self.assertEqual(devices[0]['deviceID'], '64:0d:50:d6:0b:c7')

        with self.assertRaises(AttributeError):
            self.client.core.ngfw_traffic(interval='foobar')
