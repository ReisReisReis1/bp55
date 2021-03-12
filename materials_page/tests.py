"""
Tests for the functions in the App: materials_page
"""
# pylint: disable=all
import io
import zipfile
from django.core.files.uploadedfile import SimpleUploadedFile


from django.test import Client
from django.test import TestCase
from materials_page.models import Material, Category
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
        test1 = Category.objects.create(name='TestKategorie1')
        test2 = Category.objects.create(name='TestKategorie2')

        Material.objects.create(name='TestDatei1', file='/media/material/Test1.pdf', category=test1)
        Material.objects.create(name='TestDatei2', file='/media/material/Test2.pdf', category=test1)
        Material.objects.create(name='TestDatei3', file='/media/material/Test3.pdf', category=test2)
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

        test1 = Category.objects.create(name='TestKategorie1')
        test2 = Category.objects.create(name='TestKategorie2')
        test3 = Category.objects.create(name='')

        Material.objects.create(name='TestDatei1', file='/media/material/Test1.pdf', category=test1)
        Material.objects.create(name='TestDatei2', file='/media/material/Test2.pdf', category=test1)
        Material.objects.create(name='TestDatei3', file='/media/material/Test3.pdf', category=test2)
        Material.objects.create(name='', category=test3)

        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][0].name, 'TestDatei1')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][1].name, 'TestDatei2')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie2'][0].name, 'TestDatei3')
        self.assertEqual(get_categories_and_corresponding_files()[''][0].name, '')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][0].file, '/media/material/Test1.pdf')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][1].file, '/media/material/Test2.pdf')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie2'][0].file, '/media/material/Test3.pdf')
        self.assertEqual(get_categories_and_corresponding_files()[''][0].file, '')
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][0].category, test1)
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie1'][1].category, test1)
        self.assertEqual(get_categories_and_corresponding_files()['TestKategorie2'][0].category, test2)
        self.assertEqual(get_categories_and_corresponding_files()[''][0].category, test3)

    def test3_get_categories_and_corresponding_zip_files(self):
        """
        Testing the get_catgeories_and_corresponding_files function


        self.assertEqual(get_categories_and_corresponding_zip_files(), {})

        Material.objects.create(name='TestDatei1',
                                file='C:/Users/Laura Buhleier/Documents/GitHub/media/Test1.pdf',
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
        """

    def test4_get_category(self):
        """
        Testing the get_category function
        """
        test1 = Category.objects.create(name='TestKategorie1')
        test2 = Category.objects.create(name='TestKategorie2')
        test3 = Category.objects.create(name='')

        test4 = Category.objects.create(name='TestKategorie3')
        test5 = Category.objects.create(name='TestKategorie3')

        testmat1 = Material.objects.create(name='TestDatei1', file='/media/material/Test1.pdf', category=test1)
        testmat2 = Material.objects.create(name='TestDatei2', file='/media/material/Test2.pdf', category=test1)
        testmat3 = Material.objects.create(name='TestDatei3', file='/media/material/Test3.pdf', category=test2)
        testmat4 = Material.objects.create(name='', category=test3)

        testmat5 = Material.objects.create(name='TestDatei5', category=test4)
        testmat6 = Material.objects.create(name='TestDatei6', category=test4)
        testmat7 = Material.objects.create(name='TestDatei7', category=test5)
        testmat8 = Material.objects.create(name='TestDatai8',)

        self.assertEqual(testmat1.get_category(), 'TestKategorie1')
        self.assertEqual(testmat2.get_category(), 'TestKategorie1')
        self.assertEqual(testmat3.get_category(), 'TestKategorie2')
        self.assertEqual(testmat4.get_category(), '')
        self.assertEqual(testmat5.get_category(), 'TestKategorie3')
        self.assertEqual(testmat6.get_category(), 'TestKategorie3')
        self.assertEqual(testmat7.get_category(), 'TestKategorie3')
        self.assertEqual(testmat8.get_category(), 'Sonstiges')

    def test_views(self):
        test1 = Category.objects.create(name='TestKategorie1')

        test2 = Category.objects.create(name='TestKategorie2')

        test3 = Category.objects.create(name='')

        test4 = Category.objects.create(name='TestKategorie3')
        test5 = Category.objects.create(name='TestKategorie3')

        Material.objects.create(name='TestDatei1', file='/media/material/Test1.pdf', category=test1)
        response = self.client.get('/materials_page/')
        print(response)
        Material.objects.create(name='TestDatei2', file='/media/material/Test2.pdf', category=test1)
        Material.objects.create(name='TestDatei3', file='/media/material/Test3.pdf', category=test2)
        Material.objects.create(name='', category=test3)

        response = self.client.get('/materials_page/')
        print(response)

        testmat5 = Material.objects.create(name='TestDatei5', category=test4)
        testmat6 = Material.objects.create(name='TestDatei6', category=test4)
        testmat7 = Material.objects.create(name='TestDatei7', category=test5)
        testmat8 = Material.objects.create(name='TestDatai8', )

        # response = self.client.get('/materials_page/')
        # self.assertEqual(response.status_code, 200)
        # print(response.context['Materials'])


class CategoryTestCases(TestCase):
    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1__str__(self):
        """
        Testing the __str__ function
        """
        Category.objects.create(name='TestKategorie1')
        Category.objects.create(name='')

        test1 = Category.objects.get(name='TestKategorie1').__str__()
        test2 = Category.objects.get(name='').__str__()

        self.assertEqual('TestKategorie1', test1)
        self.assertEqual('', test2)
