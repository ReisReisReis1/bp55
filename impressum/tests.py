"""
Tests for the functions in the App: impressum
"""
# pylint: disable = import-error
from django.test import Client, TestCase
from impressum.models import Impressum
from impressum.views import get_course_link


class ImpressumTestCases(TestCase):
    """
    Test Cases for the functions used in Impressum
    """

    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1__str__(self):
        """
        Testing the __str__ function
        """
        impressum1 = Impressum(name='Impressum',
                               course_link='ruinsandbeyond.architektur.tu-darmstadt.de')
        test1 = impressum1.__str__()
        self.assertEqual(test1, 'Impressum')

    def test3_get_course_link(self):
        """
        Testing the get_course_link function
        """
        self.assertEqual(get_course_link(), '')
        Impressum.objects.create(name='Impressum',
                                 course_link='ruinsandbeyond.architektur.tu-darmstadt.de')
        self.assertEqual(get_course_link(), 'ruinsandbeyond.architektur.tu-darmstadt.de')

    def test_views(self):
        """
        Testing the function impressum in views
        """
        Impressum.objects.create(name='Impressum',
                                 course_link='ruinsandbeyond.architektur.tu-darmstadt.de')
        response = self.client.get('/impressum/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Kurs_Link'],
                         'ruinsandbeyond.architektur.tu-darmstadt.de')
