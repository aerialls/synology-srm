# -*- coding: utf-8 -*-

from synology_srm.api import Api


class ApiBase(Api):
    """API Base.

    Handles the SYNO.API API namespace.
    """

    def info(self):
        """Gets the API info list."""
        return self.http.call(
            path='query.cgi',
            api='SYNO.API.Info',
            method='query',
            version=1,
            params={
                'query': 'ALL',
            },
            restricted=False,
        )

    def encryption(self):
        """Gets the API encryption."""
        return self.http.call(
            path='encryption.cgi',
            api='SYNO.API.Encryption',
            method='getinfo',
            version=1,
        )
