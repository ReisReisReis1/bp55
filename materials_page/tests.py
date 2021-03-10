"""
Tests for the functions in the App: materials_page
"""
# pylint: disable=all
import io
import zipfile
from django.core.files.uploadedfile import SimpleUploadedFile


from django.test import Client
from django.test import TestCase
from materials_page.models import Material
from materials_page.views import get_categories_and_corresponding_files, get_categories_and_corresponding_zip_files


class MaterialTestCases(TestCase):
    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1__str__(self):
        """
        Testing the __str__ function
        """

        Material.objects.create(name='TestDatei1', file='/media/material/Test1.pdf', category='TestKategorie1')
        Material.objects.create(name='TestDatei2', file='/media/material/Test2.pdf', category='TestKategorie1')
        Material.objects.create(name='TestDatei3', file='/media/material/Test3.pdf', category='TestKategorie2')
        Material.objects.create(name='')

        test1 = Material.objects.get(name='TestDatei1').__str__()
        test2 = Material.objects.get(name='TestDatei2').__str__()
        test3 = Material.objects.get(name='TestDatei3').__str__()
        test4 = Material.objects.get(name='').__str__()
        self.assertEqual(test1, 'TestDatei1')
        self.assertEqual(test2, 'TestDatei2')
        self.assertEqual(test3, 'TestDatei3')
        self.assertEqual(test4, '')

    def test2_get_categories_and_corresponding_files(self):
        """
        Testing the get_catgeories_and_corresponding_files function
        """

        self.assertEqual(get_categories_and_corresponding_files(), {})

        Material.objects.create(name='TestDatei1', file='/media/material/Test1.pdf', category='TestKategorie1')
        Material.objects.create(name='TestDatei2', file='/media/material/Test2.pdf', category='TestKategorie1')
        Material.objects.create(name='TestDatei3', file='/media/material/Test3.pdf', category='TestKategorie2')
        Material.objects.create(name='')

        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][0].name, 'TestDatei1')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][1].name, 'TestDatei2')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie2'][0].name, 'TestDatei3')
        self.assertEqual(get_categories_and_corresponding_files()[''][0].name, '')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][0].file, '/media/material/Test1.pdf')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][1].file, '/media/material/Test2.pdf')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie2'][0].file, '/media/material/Test3.pdf')
        self.assertEqual(get_categories_and_corresponding_files()[''][0].file, '')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][0].category, 'TestKategorie1')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][1].category, 'TestKategorie1')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie2'][0].category, 'TestKategorie2')
        self.assertEqual(get_categories_and_corresponding_files()[''][0].category, '')

    def test3_get_categories_and_corresponding_zip_files(self):
        """
        Testing the get_catgeories_and_corresponding_files function
        """

        self.assertEqual(get_categories_and_corresponding_zip_files(), {})

        Material.objects.create(name='TestDatei1', file='C:/Users/Laura Buhleier/Documents/GitHub/media/Test1.pdf',
                                category='TestKategorie1')
        Material.objects.create(name='TestDatei2', file='C:/Users/Laura Buhleier/Documents/GitHub/media/Test2.pdf',
                                category='TestKategorie1')
        Material.objects.create(name='TestDatei3', file='C:/Users/Laura Buhleier/Documents/GitHub/media/Test3.pdf',
                                category='TestKategorie2')

        try:
            file = io.BytesIO(get_categories_and_corresponding_zip_files()['TestKategorie1'].content)
            zipped_file = zipfile.ZipFile(file, 'r')
            self.assertIsNone(zipped_file.testzip())
            self.assertIn('zipfiles/Test1.pdf', zipped_file.namelist())
            self.assertIn('zipfiles/Test2.pdf', zipped_file.namelist())
        finally:
            zipped_file.close()
            file.close()
        try:
            file = io.BytesIO(get_categories_and_corresponding_zip_files()['TestKategorie2'].content)
            zipped_file = zipfile.ZipFile(file, 'r')
            self.assertIsNone(zipped_file.testzip())
            self.assertIn('zipfiles/Test3.pdf', zipped_file.namelist())
        finally:
            zipped_file.close()
            file.close()





