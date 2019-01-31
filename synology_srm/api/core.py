# -*- coding: utf-8 -*-

from synology_srm.api import Api


class ApiCore(Api):
    """API Core.

    Handles the SYNO.Core API namespace.
    """

    def system_utilization(self):
        """Gets the system utilization.
        {
            "cpu": {
                [...]
            },
            "disk": {
                [...]
            },
            "memory": {
                [...]
            },
            "network": [
                [...]
            ],
            "space": {
                [...]
            },
            "time": [...]
        }
        """
        return self.http.call(
            path='entry.cgi',
            api='SYNO.Core.System.Utilization',
            method='get',
            version=1,
        )
