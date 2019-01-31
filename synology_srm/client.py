# -*- coding: utf-8 -*-

from synology_srm.http import Http
from synology_srm.api.core import ApiCore
from synology_srm.api.mesh import ApiMesh


class Client(object):
    """Main entry point for using the API.

    You can access namespaces directly with client.<namespace>.<method>()
    """

    def __init__(self, host: str, port: int,
                 username: str, password: str, https: bool = True):
        self.http = Http(
            host=host,
            port=port,
            username=username,
            password=password,
            https=https,
        )

        self.api = {
            'core': ApiCore(self.http),
            'mesh': ApiMesh(self.http),
        }

    def __getattr__(self, item):
        return self.api[item]
