# -*- coding: utf-8 -*-

import unittest
import requests_mock
import synology_srm

class TestMesh(unittest.TestCase):
    def setUp(self):
        """Set up things to be run when tests are started."""
        self.client = synology_srm.Client(
            host='192.168.1.254',
            port=8001,
            username='admin',
            password='admin'
        )

        self.http = self.client.http

    def _mock_login(self, m):
        m.get('{}/auth.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'sid': 'Sylgv43ED9AAECBBFD5C08D1D'
            },
            'success': True
        })

    @requests_mock.Mocker()
    def test_network_wifidevice(self, m):
        self._mock_login(m)
        m.get('{}/entry.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'devices': [
                    {
                        'band': '5G',
                        'connection': 'wifi',
                        'current_rate': 780,
                        'hostname': 'iPad',
                        'is_guest': False,
                        'mac': '08:f6:9c:0b:7e:8e',
                        'max_rate': 866,
                        'mesh_node_id': 0,
                        'netif': 'wlan1',
                        'rate_quality': 'high',
                        'signalstrength': 56,
                        'transferRX': 7876940,
                        'transferRX_rate': 0,
                        'transferTX': 269652361,
                        'transferTX_rate': 0
                    },
                    {
                        'band': '5G',
                        'connection': 'wifi',
                        'current_rate': 866,
                        'hostname': 'OnePlus 6T',
                        'is_guest': False,
                        'mac': '64:a2:f9:7a:ce:0a',
                        'max_rate': 866,
                        'mesh_node_id': 0,
                        'netif': 'wlan1',
                        'rate_quality': 'high',
                        'signalstrength': 93,
                        'transferRX': 2313469,
                        'transferRX_rate': 0,
                        'transferTX': 41262501,
                        'transferTX_rate': 0
                    }
                ]
            },
            'success': True
        })

        devices = self.client.mesh.network_wifidevice()

        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]['hostname'], 'iPad')
        self.assertEqual(devices[1]['mac'], '64:a2:f9:7a:ce:0a')

        self.http.sid = None
