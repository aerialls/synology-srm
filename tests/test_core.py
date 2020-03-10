# -*- coding: utf-8 -*-

import filecmp
import os
import requests_mock
import tempfile

from tests.api import TestCaseApi
from tests.payload import (
    GET_NETWORK_NSM_DEVICE_PAYLOAD,
    GET_SYSTEM_UTILIZATION_PAYLOAD,
    LIST_DDNS_EXTIP_PAYLOAD,
    LIST_DDNS_RECORD_PAYLOAD,
    GET_NGFW_TRAFFIC_PAYLOAD,
    LIST_CERTIFICATE_PAYLOAD,
)


class TestCore(TestCaseApi):

    @requests_mock.Mocker()
    def test_get_system_utilization(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=GET_SYSTEM_UTILIZATION_PAYLOAD,
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
            json=LIST_DDNS_EXTIP_PAYLOAD,
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
            json=LIST_DDNS_RECORD_PAYLOAD,
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
            json=GET_NETWORK_NSM_DEVICE_PAYLOAD,
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
            json=GET_NGFW_TRAFFIC_PAYLOAD,
        )

        devices = self.client.core.get_ngfw_traffic(interval='live')

        self.assertEqual(len(devices), 3)
        self.assertEqual(devices[0]['deviceID'], '64:0d:50:d6:0b:c7')

        with self.assertRaises(AttributeError):
            self.client.core.ngfw_traffic(interval='foobar')

    @requests_mock.Mocker()
    def test_list_certificate(self, m):
        self._mock_login(m)
        m.get(
            '{}/entry.cgi'.format(self.http._get_base_url()),
            json=LIST_CERTIFICATE_PAYLOAD
        )

        certificates = self.client.core.list_certificate()
        self.assertEqual(certificates[0]['issuer']['common_name'], 'Madalynn Paris')

        self.assertEqual(len(certificates), 3)

    @requests_mock.Mocker()
    def test_export_certificate(self, m):
        self._mock_login(m)
        crt_raw_file = os.path.join(os.path.dirname(__file__), 'data', 'certificate.zip')
        with open(crt_raw_file, 'rb') as zip:
            m.get(
                '{}/entry.cgi'.format(self.http._get_base_url()),
                content=zip.read(),
                headers={
                    'Content-Type': 'application/zip'
                },

            )

        crt_downloaded_file = tempfile.mktemp()
        self.client.core.export_certificate(crt_downloaded_file)

        # Both files should be the same
        self.assertTrue(filecmp.cmp(crt_raw_file, crt_downloaded_file))

        os.remove(crt_downloaded_file)
