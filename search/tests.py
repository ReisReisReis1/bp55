"""
Tests for the functions in the App: search
"""

from django.test import TestCase, Client
from model_bakery import baker


class SearchTest(TestCase):
    """

    """
    def setUp(self):
        """

        """
        self.client = Client()
        self.test1 = baker.make('details_page.Building')
        self.test2 = baker.make('details_page.Building')
        self.test3 = baker.make('details_page.Building')
        self.test4 = baker.make('details_page.Building')
        self.test5 = baker.make('details_page.Building')

    def test1_search(self):
        """

        """
        response = self.client.get('/search/?search_request=')
        self.assertEqual(list(response.context['Result']),
                         [self.test1, self.test2, self.test3, self.test4, self.test5])
