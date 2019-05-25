# -*- coding: utf-8 -*-

from synology_srm.api import Api


class ApiCore(Api):
    """API Core.

    Handles the SYNO.Core API namespace.
    """

    def system_utilization(self):
        """Gets the system utilization."""
        return self.http.call(
            path='entry.cgi',
            api='SYNO.Core.System.Utilization',
            method='get',
            version=1,
        )

    def ddns_extip(self):
        """Gets the external IP address."""
        return self.http.call(
            path='entry.cgi',
            api='SYNO.Core.DDNS.ExtIP',
            method='list',
            version=1,
        )

    def ddns_record(self):
        """Gets the DDNS record."""
        return self.http.call(
            path='entry.cgi',
            api='SYNO.Core.DDNS.Record',
            method='list',
            version=1,
        )

    def network_nsm_device(self, filters={}):
        """Gets the network NSM device."""
        response = self.http.call(
            path='entry.cgi',
            api='SYNO.Core.Network.NSM.Device',
            method='get',
            version=1,
        )

        return self._filter(response['devices'], filters)
