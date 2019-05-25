# -*- coding: utf-8 -*-

from synology_srm.http import Http


class Api(object):
    """API.

    Base class for all API namespaces.
    """

    def __init__(self, http: Http):
        self.http = http

    def _filter(self, elements, filters):
        """Filter elements with a list of constraints
        Each filter needs to be evaluate to true to return the element
        """
        if not isinstance(filters, dict) or not filters:
            return elements

        def _filter_element(element, filters):
            for key, value in filters.items():
                if element[key] != value:
                    return False
            return True

        return list(filter(lambda e: _filter_element(e, filters), elements))
