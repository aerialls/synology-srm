# -*- coding: utf-8 -*-

from synology_srm.api.base import ApiBase


class ApiMesh(ApiBase):
    """API Mesh.

    Handles the SYNO.Mesh API namespace.
    """

    def network_wanstatus(self):
        """Gets the network WAN status.
        {
            "wan_connected": true
        }
        """
        return self.http.call(
            path='entry.cgi',
            api='SYNO.Mesh.Network.WANStatus',
            method='get',
            version=1
        )

    def network_wifidevice(self):
        """Gets the network Wi-Fi devices.
        {
            "devices": [
            {
                "band": "[...]",
                "connection": "[...]",
                "current_rate": [...],
                "hostname": "[...]",
                "is_guest": false,
                "mac": "[...]",
                "max_rate": [...],
                "mesh_node_id": [...],
                "netif": "[...]",
                "rate_quality": "[...]",
                "signalstrength": [...],
                "transferRX": [...],
                "transferRX_rate": [...],
                "transferTX": [...],
                "transferTX_rate": [...]
            },
            [...]
        }
        """
        response = self.http.call(
            path='entry.cgi',
            api='SYNO.Mesh.Network.WifiDevice',
            method='get',
            version=1
        )

        return response['devices']
