"""
Tests for the functions in the App: impressum
"""
# pylint disable=all
from django.test import Client
from django.test import TestCase
from impressum.models import Impressum
from impressum.views import get_course_link
from django.core.exceptions import ValidationError


class ImpressumTestCases(TestCase):
    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1__str__(self):
        """
        Testing the __str__ function
        """
        Impressum.objects.create(name='Impressum', course_link= 'ruinsandbeyond.architektur.tu-darmstadt.de')
        test1 = Impressum.objects.get(name='Impressum').__str__()
        self.assertEqual(test1, 'Impressum')

    def test2_save(self):
        """
        Testing the save function
        """
        Impressum.objects.create(name='Impressum', course_link='ruinsandbeyond.architektur.tu-darmstadt.de')
        # self.assertEqual(Impressum.objects.create(name='', course_link=''), ValidationError)
        # self.assertEqual(Impressum.objects.create(name='Impressum2', course_link='moodle.tu-darmstadt.de'),
                         # ValidationError)

    def test3_get_course_link(self):
        """
        Testing the get_course_link function
        """
        self.assertEqual(get_course_link(), '')
        Impressum.objects.create(name='Impressum', course_link='ruinsandbeyond.architektur.tu-darmstadt.de')
        self.assertEqual(get_course_link(), 'ruinsandbeyond.architektur.tu-darmstadt.de')