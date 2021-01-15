"""
Tests for functions in the App: start
"""

from django.test import Client
from django.test import TestCase
from video_content.models import Video


class ViewsTestCases(TestCase):
    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1(self):
        """
        Testing start function in views
        """
        Video.objects.create(title='Test8', video='/media/videos/Intro2.mp2', era='Sonstiges', intro=True)
        response = self.client.get('/start/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['video'], Video.get_intro(Video))

