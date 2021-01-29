"""
Tests for functions in the App: start
"""
# pylint: disable=all
from django.test import Client
from django.test import TestCase
from video_content.models import Video
from details_page.models import Era


class ViewsTestCases(TestCase):
    """
    Tests if the intro page with the intro video is loading correctly
    """

    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1(self):
        # pylint: disable=no-member
        """
        Testing start function in views
        """
        Video.objects.create(title='Test8', video='/media/videos/Intro2.mp2',
                             era=Era.objects.create(), intro=True)
        response = self.client.get('/start/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Video'], Video.get_intro(Video))
