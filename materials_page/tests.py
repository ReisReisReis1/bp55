"""
Tests for the functions in the App: materials_page
"""
# pylint: disable=all
from django.test import Client
from django.test import TestCase
from materials_page.models import Material


class MaterialTestCases(TestCase):
    def setUp(self):
        """
        Setting up objects and a client for the tests
        """
        self.client = Client()
        Material.objects.create(name='TestDatei1', file='/media/material/Test1.pdf', category='TestKategorie1')
        Material.objects.create(name='TestDatei2', file='/media/material/Test2.pdf', category='TestKategorie1')
        Material.objects.create(name='TestDatei3', file='/media/material/Test3.pdf', category='TestKategorie2')
        Material.objects.create(name='')

    def test1__str__(self):
        """
        Testing the __str__ function
        """
        test1 = Material.objects.get(name='TestDatei1').__str__()
        test2 = Material.objects.get(name='TestDatei2').__str__()
        test3 = Material.objects.get(name='TestDatei3').__str__()
        test4 = Material.objects.get(name='').__str__()
        self.assertEqual(test1, 'TestDatei1')
        self.assertEqual(test2, 'TestDatei2')
        self.assertEqual(test3, 'TestDatei3')
        self.assertEqual(test4, '')

    def test2_get_category(self):
        """
        Testing the get_category function
        """
        self.assertEqual(list(Material.get_category(Material, 'TestKategorie1')),
                         list(Material.objects.filter(category='TestKategorie1')))
        self.assertEqual(list(Material.get_category(Material, 'TestKategorie2')),
                         list(Material.objects.filter(category='TestKategorie2')))
        self.assertEqual(list(Material.get_category(Material, '')),
                         list(Material.objects.filter(category='')))

