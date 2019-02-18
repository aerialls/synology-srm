# -*- coding: utf-8 -*-

import requests_mock

from tests.api import TestCaseApi


class TestMesh(TestCaseApi):

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

    @requests_mock.Mocker()
    def test_network_wanstatus(self, m):
        self._mock_login(m)
        m.get('{}/entry.cgi'.format(self.http._get_base_url()), json={
            'data': {
                "wan_connected": True
            },
            'success': True
        })

        wanstatus = self.client.mesh.network_wanstatus()
        self.assertEqual(wanstatus['wan_connected'], True)

        self.http.sid = None

    @requests_mock.Mocker()
    def test_system_info(self, m):
        self._mock_login(m)
        m.get('{}/entry.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'nodes': [
                    {
                        'firmware_ver': 'SRM 1.2-7742 Update 5',
                        'is_re': False,
                        'model': 'RT2600ac',
                        'node_id': 0,
                        'sn': '176XXXXXX01',
                        'unique': 'synology_xxxxxx_rt2600ac',
                        'uptime': 1833868
                    }
                ],
                'total': 1
            },
            'success': True
        })

        system_info = self.client.mesh.system_info()
        self.assertEqual(
            system_info['nodes'][0]['firmware_ver'],
            "SRM 1.2-7742 Update 5",
        )

        self.http.sid = None
