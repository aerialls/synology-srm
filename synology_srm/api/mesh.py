# -*- coding: utf-8 -*-

from synology_srm.api import Api


class ApiMesh(Api):
    """API Mesh.

    Handles the SYNO.Mesh API namespace.
    """

    def network_wanstatus(self):
        """Gets the network WAN status."""
        return self.http.call(
            path='entry.cgi',
            api='SYNO.Mesh.Network.WANStatus',
            method='get',
            version=1,
        )

    def network_wifidevice(self):
        """Gets the network Wi-Fi devices."""
        response = self.http.call(
            path='entry.cgi',
            api='SYNO.Mesh.Network.WifiDevice',
            method='get',
            version=1,
        )

        return response['devices']
