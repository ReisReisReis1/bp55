"""
Tests for functions in the App: home
"""

from django.test import Client
from django.test import TestCase


class ViewsTestCases(TestCase):
    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1(self):
        """
        Testing building_filter function in views
        """
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 200)
