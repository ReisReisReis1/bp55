"""
Tests for functions in the App: home
"""

from django.test import Client, TestCase
from model_bakery import baker


class ViewsTestCases(TestCase):
    """
    Testcases for the functions in view
    """

    def setUp(self):
        """
        Setting up a client, some buildings and eras for the tests
        """
        self.client = Client()
        self.test1 = baker.make('details_page.Building')
        self.test2 = baker.make('details_page.Building')
        self.test3 = baker.make('details_page.Building')
        self.test4 = baker.make('details_page.Building')
        self.test5 = baker.make('details_page.Building')

    def test1(self):
        """
        Testing building_filter function in views
        """
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 200)

