# -*- coding: utf-8 -*-

from synology_srm.http import Http


class ApiBase(object):
    """API base.

    Base class for all API namespaces.
    """

    def __init__(self, http: Http):
        self.http = http
