# -*- coding: utf-8 -*-

import os

from synology_srm.api import Api

INTERVAL_VALUES = ['live', 'day', 'week', 'month']

class ApiCore(Api):
    """API Core.

    Handles the SYNO.Core API namespace.
    """

    def get_system_utilization(self):
        """Gets the system utilization."""
        return self.http.call(
            endpoint='entry.cgi',
            api='SYNO.Core.System.Utilization',
            method='get',
            version=1,
        )

    def list_ddns_extip(self):
        """Gets the external IP address."""
        return self.http.call(
            endpoint='entry.cgi',
            api='SYNO.Core.DDNS.ExtIP',
            method='list',
            version=1,
        )

    def list_ddns_record(self):
        """Gets the DDNS record."""
        return self.http.call(
            endpoint='entry.cgi',
            api='SYNO.Core.DDNS.Record',
            method='list',
            version=1,
        )

    def get_network_nsm_device(self, filters={}):
        """Gets the network NSM device."""
        response = self.http.call(
            endpoint='entry.cgi',
            api='SYNO.Core.Network.NSM.Device',
            method='get',
            version=1,
        )

        return self._filter(response['devices'], filters)

    def get_ngfw_traffic(self, interval):
        """Gets network traffic statistics for the specified interval."""
        if interval not in INTERVAL_VALUES:
            raise AttributeError('Interval unknown, must be one of {}'.format(INTERVAL_VALUES))

        params = {
            'mode': 'net_l7',
            'interval': interval
        }

        return self.http.call(
            endpoint='entry.cgi',
            api='SYNO.Core.NGFW.Traffic',
            method='get',
            params=params,
            version=1,
        )

    def list_certificate(self):
        """List all TLS certificates."""
        response = self.http.call(
            endpoint='entry.cgi',
            api='SYNO.Core.Certificate',
            method='list',
            version=1,
        )

        return response['certificates']

    def export_certificate(self, path='certificate.zip'):
        """Export/download the TLS certificate."""
        return self.http.download(
            endpoint='entry.cgi',
            api='SYNO.Core.Certificate',
            method='export',
            version=1,
            path=path,
            params={
                # If it's not "archive", the export will fail
                # with the error 117
                'file': '"archive"',
            },
        )
