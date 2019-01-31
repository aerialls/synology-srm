# -*- coding: utf-8 -*-

import unittest
import requests_mock
import synology_srm


class TestCore(unittest.TestCase):
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
    def test_system_utilization(self, m):
        self._mock_login(m)
        m.get('{}/entry.cgi'.format(self.http._get_base_url()), json={
            'data': {
                'cpu': {
                    '15min_load': 8,
                    '1min_load': 19,
                    '5min_load': 9,
                    'device': 'System',
                    'other_load': 1,
                    'system_load': 6,
                    'user_load': 1
                },
                'disk': {
                    'disk': [],
                    'total': {
                        'device': 'total',
                        'read_access': 0,
                        'read_byte': 0,
                        'utilization': 0,
                        'write_access': 0,
                        'write_byte': 0
                    }
                },
                'memory': {
                    'avail_real': 109484,
                    'avail_swap': 260332,
                    'buffer': 67712,
                    'cached': 122960,
                    'device': 'Memory',
                    'memory_size': 524288,
                    'real_usage': 36,
                    'si_disk': 0,
                    'so_disk': 0,
                    'swap_usage': 0,
                    'total_real': 471324,
                    'total_swap': 262140
                },
                'network': [
                    {
                        'device': 'total',
                        'rx': 41741,
                        'tx': 42506
                    },
                    {
                        'device': 'bwlan0',
                        'rx': 0,
                        'tx': 0
                    },
                    {
                        'device': 'bwlan1',
                        'rx': 0,
                        'tx': 0
                    },
                    {
                        'device': 'eth0',
                        'rx': 37766,
                        'tx': 4359
                    },
                    {
                        'device': 'lbr0',
                        'rx': 3975,
                        'tx': 38147
                    }
                ],
                'space': {
                    'lun': [],
                    'total': {
                        'device': 'total',
                        'read_access': 0,
                        'read_byte': 0,
                        'utilization': 0,
                        'write_access': 0,
                        'write_byte': 1265
                    },
                    'volume': [
                        {
                            'device': 'mmcblk0p6',
                            'display_name': 'volume1',
                            'read_access': 0,
                            'read_byte': 0,
                            'utilization': 0,
                            'write_access': 0,
                            'write_byte': 1265
                        }
                    ]
                },
                'time': 1548882854
            },
            'success': True
        })

        system_utilization = self.client.core.system_utilization()

        self.assertEqual(system_utilization['cpu']['5min_load'], 9)
        self.assertEqual(system_utilization['memory']['avail_swap'], 260332)

        self.http.sid = None
