# -*- coding: utf-8 -*-

import unittest

from unittest.mock import patch
from synology_srm import Client

class TestHomeAssistant(unittest.TestCase):
    def setUp(self):
        """Set up things to be run when tests are started."""
        self.client = Client(
            host='192.168.1.254',
            port=8001,
            username='admin',
            password='admin'
        )

    def test_initial_state(self):
        self.assertIs(self.client.http.sid, None)
