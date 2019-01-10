from synology_srm import Http


class ApiMesh(object):

    def __init__(self, http: Http):
        self.http = http

    def network_wifidevice(self):
        response = self.http.call(
            path='entry.cgi',
            api='SYNO.Mesh.Network.WifiDevice',
            method='get',
            version=1
        )

        return response['devices']
