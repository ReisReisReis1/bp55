"""
Tests for functions in the App: timeline
"""

from django.test import Client
from django.test import TestCase


class ViewsTestCases(TestCase):
    """
     Testcases for the functions in view
    """
    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1(self):
        """
        Testing timeline function in views
        """
        response = self.client.get('/timeline/')
        self.assertEqual(response.status_code, 200)
