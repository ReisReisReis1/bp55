"""
Tests for the functions in the App: details_page
"""
from django.test import Client
from django.test import TestCase
from details_page.models import Building
from details_page.models import Era
from details_page.models import Picture
from details_page.models import Blueprint

class BuildingTestCases(TestCase):
    def setUp(self):
        """
        Setting up objects and a client for the tests
        """
        self.client = Client()
        test_era=Era.objects.create(name='Frühe Kaiserzeit', year_from=55, year_from_BC_or_AD='v.Chr', year_to=55,
                           year_to_BC_or_AD='v.Chr')
        Building.objects.create(pk=0, name='', city='', region='', country='', date_from=0, date_from_BC_or_AD='',
                                 date_to=0, date_to_BC_or_AD='', era=test_era, architect='', context='', builder='',
                                 construction_type='', design='', function='', length=0, width=0, height=0,
                                 circumference=0, area=0, column_order='', construction='', material='',
                                 literature='')
        Building.objects.create(pk=1, name='Parthenon', city='Athen', region='TestRegion', country='GR-Griechenland',
                                date_from=447, date_from_BC_or_AD='v.Chr.', date_to=438, date_to_BC_or_AD='v.Chr.',
                                era=test_era, architect='Iktinos, Kallikrates', context='Tempel',
                                builder='Perikles und die Polis Athen', construction_type='Tempel',
                                design='Peripteros', function='Sakralbau', length=30.88, width=69.5, height=1,
                                circumference=1, area=1, column_order='dorisch, ionischer Fries',
                                construction='Massivbau', material='penetelischer Marmor',
                                literature='Muss - Schubert 1988, SEITEN?; Gruben 2001, 173-190; Hellmann 2006, 82-96;')


    def test1_get_name(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_name(Building, 0), '')
        self.assertEqual(Building.get_name(Building, 1), 'Parthenon')

    def test2_get_city(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_city(Building, 0), '')
        self.assertEqual(Building.get_city(Building, 1), 'Athen')

    def test3_get_region(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_region(Building, 0), '')
        self.assertEqual(Building.get_region(Building, 1), 'TestRegion')

    def test4_get_country(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_country(Building, 0), '')
        self.assertEqual(Building.get_country(Building, 1), 'GR-Griechenland')

    def test5_get_date_from(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_date_from(Building, 0), 0)
        self.assertEqual(Building.get_date_from(Building, 1), 447)

    def test6_get_date_from_BC_or_AD(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_date_from_BC_or_AD(Building, 0), '')
        self.assertEqual(Building.get_date_from_BC_or_AD(Building, 1), 'v.Chr.')

    def test7_get_date_to(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_date_to(Building, 0), 0)
        self.assertEqual(Building.get_date_to(Building, 1), 438)

    def test8_get_date_to_BC_or_AD(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_date_to_BC_or_AD(Building, 0), '')
        self.assertEqual(Building.get_date_to_BC_or_AD(Building, 1), 'v.Chr.')

    def test9_get_architect(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_architect(Building, 0), '')
        self.assertEqual(Building.get_architect(Building, 1), 'Iktinos, Kallikrates')

    def test10_get_context(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_context(Building, 0), '')
        self.assertEqual(Building.get_context(Building, 1), 'Tempel')

    def test11_get_builder(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_builder(Building, 0), '')
        self.assertEqual(Building.get_builder(Building, 1), 'Perikles und die Polis Athen')

    def test12_get_construction_type(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_construction_type(Building, 0), '')
        self.assertEqual(Building.get_construction_type(Building, 1), 'Tempel')

    def test13_get_design(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_design(Building, 0), '')
        self.assertEqual(Building.get_design(Building, 1), 'Peripteros')

    def test14_get_function(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_function(Building, 0), '')
        self.assertEqual(Building.get_function(Building, 1), 'Sakralbau')

    def test15_get_length(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_length(Building, 0), 0)
        self.assertEqual(Building.get_length(Building, 1), 30.88)

    def test16_get_width(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_width(Building, 0), 0)
        self.assertEqual(Building.get_width(Building, 1), 69.5)

    def test17_get_height(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_height(Building, 0), 0)
        self.assertEqual(Building.get_height(Building, 1), 1)

    def test18_get_circumference(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_circumference(Building, 0), 0)
        self.assertEqual(Building.get_circumference(Building, 1), 1)

    def test19_get_area(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_area(Building, 0), 0)
        self.assertEqual(Building.get_area(Building, 1), 1)

    def test20_get_column_order(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_column_order(Building, 0), '')
        self.assertEqual(Building.get_column_order(Building, 1), 'dorisch, ionischer Fries')

    def test21_get_construction(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_construction(Building, 0), '')
        self.assertEqual(Building.get_construction(Building, 1), 'Massivbau')

    def test22_get_material(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_material(Building, 0), '')
        self.assertEqual(Building.get_material(Building, 1), 'penetelischer Marmor')

    def test23_get_literature(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_literature(Building, 0), '')
        self.assertEqual(Building.get_literature(Building, 1),
                         'Muss - Schubert 1988, SEITEN?; Gruben 2001, 173-190; Hellmann 2006, 82-96;')

    def test24__str__(self):
        """
        Testing the __str__ function
        """
        test1=Building.objects.get(name='').__str__()
        test2=Building.objects.get(name='Parthenon').__str__()
        self.assertEqual(test1, '')
        self.assertEqual(test2, 'Parthenon')






