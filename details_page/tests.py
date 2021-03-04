"""
Tests for the functions in the App: details_page
"""
# pylint: disable=all
from django.test import Client
from django.test import TestCase
from django.core.exceptions import ValidationError
from details_page.models import Era, Picture, Building, Blueprint, get_year_as_signed_int, \
    validate_color_code, validate_url_conform_str
from django.core.files.uploadedfile import SimpleUploadedFile

# Define some temp images for testing
test_image = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
              b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
              b'\x02\x4c\x01\x00\x3b')  # this is one white pixel as byte code
image_mock = SimpleUploadedFile('small.img', test_image, content_type='image/gif')
image_mock2 = SimpleUploadedFile('small.img', test_image, content_type='image/gif')


class ViewsTestCases(TestCase):
    """
    Testcases for the functions in view
    """

    def setUp(self):
        """
        Setting up a client for the tests
        """
        self.client = Client()

    def test1(self):
        """
        Testing detailed function in views
        """
        building = Building.objects.create(name='Test1', pk=0)
        response = self.client.get('/details_page/' + str(building.pk) + '/')
        self.assertEqual(response.status_code, 200)


class BuildingTestCases(TestCase):
    def setUp(self):
        """
        Setting up objects and a client for the tests
        """
        self.client = Client()
        test_era = Era.objects.create(name='Frühe Kaiserzeit', year_from=55,
                                      year_from_BC_or_AD='v.Chr', year_to=55,
                                      year_to_BC_or_AD='v.Chr')
        Building.objects.create(pk=0, name='', description='', city='', region='', country='',
                                year_from=0,
                                year_from_BC_or_AD='', year_ca=False,
                                year_to=0, year_to_BC_or_AD='', era=test_era, architect='',
                                context='', builder='',
                                construction_type='', design='', function='', length=0, width=0,
                                height=0,
                                circumference=0, area=0, column_order='', construction='',
                                material='',
                                literature='', links='')
        Building.objects.create(pk=1, name='Parthenon', description='Das Parthenon in Athen',
                                city='Athen',
                                region='TestRegion', country='GR-Griechenland',
                                year_from=447, year_from_BC_or_AD='v.Chr.', year_to=438,
                                year_to_BC_or_AD='v.Chr.', year_ca=True,
                                era=test_era, architect='Iktinos, Kallikrates', context='Tempel',
                                builder='Perikles und die Polis Athen', construction_type='Tempel',
                                design='Peripteros', function='Sakralbau', length=30.88, width=69.5,
                                height=1,
                                circumference=1, area=1, column_order='dorisch, ionischer Fries',
                                construction='Massivbau', material='penetelischer Marmor',
                                literature='Muss - Schubert 1988, SEITEN?; Gruben 2001, 173-190; '
                                           'Hellmann 2006, 82-96;',
                                links='www.tu-darmstadt.de, www.architektur.tu-darmstadt.de'
                                )
        Building.objects.create(pk=2, name='empty')

    def test1_get_name(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_name(Building, 0), '')
        self.assertEqual(Building.get_name(Building, 1), 'Parthenon')
        self.assertEqual(Building.get_name(Building, 2), 'empty')
        self.assertEqual(Building.get_name(Building, 3), Building.DoesNotExist)

    def test2_get_city(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_city(Building, 0), '')
        self.assertEqual(Building.get_city(Building, 1), 'Athen')
        self.assertEqual(Building.get_city(Building, 2), None)
        self.assertEqual(Building.get_city(Building, 3), Building.DoesNotExist)

    def test3_get_region(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_region(Building, 0), '')
        self.assertEqual(Building.get_region(Building, 1), 'TestRegion')
        self.assertEqual(Building.get_region(Building, 2), None)
        self.assertEqual(Building.get_region(Building, 3), Building.DoesNotExist)

    def test4_get_country(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_country(Building, 0), '')
        self.assertEqual(Building.get_country(Building, 1), 'GR-Griechenland')
        self.assertEqual(Building.get_country(Building, 2), 'Griechenland')
        self.assertEqual(Building.get_country(Building, 3), Building.DoesNotExist)

    def test5_get_year_from(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_year_from(Building, 0), 0)
        self.assertEqual(Building.get_year_from(Building, 1), 447)
        self.assertEqual(Building.get_year_from(Building, 2), None)
        self.assertEqual(Building.get_year_from(Building, 3), Building.DoesNotExist)

    def test6_get_year_from_BC_or_AD(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_year_from_bc_or_ad(Building, 0), '')
        self.assertEqual(Building.get_year_from_bc_or_ad(Building, 1), 'v.Chr.')
        self.assertEqual(Building.get_year_from_bc_or_ad(Building, 2), 'n.Chr.')
        self.assertEqual(Building.get_year_from_bc_or_ad(Building, 3), Building.DoesNotExist)

    def test7_get_year_to(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_year_to(Building, 0), 0)
        self.assertEqual(Building.get_year_to(Building, 1), 438)
        self.assertEqual(Building.get_year_to(Building, 2), None)
        self.assertEqual(Building.get_year_to(Building, 3), Building.DoesNotExist)

    def test8_get_year_to_BC_or_AD(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_year_to_bc_or_ad(Building, 0), '')
        self.assertEqual(Building.get_year_to_bc_or_ad(Building, 1), 'v.Chr.')
        self.assertEqual(Building.get_year_to_bc_or_ad(Building, 2), 'n.Chr.')
        self.assertEqual(Building.get_year_to_bc_or_ad(Building, 3), Building.DoesNotExist)

    def test9_get_architect(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_architect(Building, 0), '')
        self.assertEqual(Building.get_architect(Building, 1), 'Iktinos, Kallikrates')
        self.assertEqual(Building.get_architect(Building, 2), None)
        self.assertEqual(Building.get_architect(Building, 3), Building.DoesNotExist)

    def test10_get_context(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_context(Building, 0), '')
        self.assertEqual(Building.get_context(Building, 1), 'Tempel')
        self.assertEqual(Building.get_context(Building, 2), None)
        self.assertEqual(Building.get_context(Building, 3), Building.DoesNotExist)

    def test11_get_builder(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_builder(Building, 0), '')
        self.assertEqual(Building.get_builder(Building, 1), 'Perikles und die Polis Athen')
        self.assertEqual(Building.get_builder(Building, 2), None)
        self.assertEqual(Building.get_builder(Building, 3), Building.DoesNotExist)

    def test12_get_construction_type(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_construction_type(Building, 0), '')
        self.assertEqual(Building.get_construction_type(Building, 1), 'Tempel')
        self.assertEqual(Building.get_construction_type(Building, 2), None)
        self.assertEqual(Building.get_construction_type(Building, 3), Building.DoesNotExist)

    def test13_get_design(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_design(Building, 0), '')
        self.assertEqual(Building.get_design(Building, 1), 'Peripteros')
        self.assertEqual(Building.get_design(Building, 2), None)
        self.assertEqual(Building.get_design(Building, 3), Building.DoesNotExist)

    def test14_get_function(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_function(Building, 0), '')
        self.assertEqual(Building.get_function(Building, 1), 'Sakralbau')
        self.assertEqual(Building.get_function(Building, 2), None)
        self.assertEqual(Building.get_function(Building, 3), Building.DoesNotExist)

    def test15_get_length(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_length(Building, 0), 0)
        self.assertEqual(Building.get_length(Building, 1), 30.88)
        self.assertEqual(Building.get_length(Building, 2), None)
        self.assertEqual(Building.get_length(Building, 3), Building.DoesNotExist)

    def test16_get_width(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_width(Building, 0), 0)
        self.assertEqual(Building.get_width(Building, 1), 69.5)
        self.assertEqual(Building.get_width(Building, 2), None)
        self.assertEqual(Building.get_width(Building, 3), Building.DoesNotExist)

    def test17_get_height(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_height(Building, 0), 0)
        self.assertEqual(Building.get_height(Building, 1), 1)
        self.assertEqual(Building.get_height(Building, 2), None)
        self.assertEqual(Building.get_height(Building, 3), Building.DoesNotExist)

    def test18_get_circumference(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_circumference(Building, 0), 0)
        self.assertEqual(Building.get_circumference(Building, 1), 1)
        self.assertEqual(Building.get_circumference(Building, 2), None)
        self.assertEqual(Building.get_circumference(Building, 3), Building.DoesNotExist)

    def test19_get_area(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_area(Building, 0), 0)
        self.assertEqual(Building.get_area(Building, 1), 1)
        self.assertEqual(Building.get_area(Building, 2), None)
        self.assertEqual(Building.get_area(Building, 3), Building.DoesNotExist)

    def test20_get_column_order(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_column_order(Building, 0), '')
        self.assertEqual(Building.get_column_order(Building, 1), 'dorisch, ionischer Fries')
        self.assertEqual(Building.get_column_order(Building, 2), None)
        self.assertEqual(Building.get_column_order(Building, 3), Building.DoesNotExist)

    def test21_get_construction(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_construction(Building, 0), '')
        self.assertEqual(Building.get_construction(Building, 1), 'Massivbau')
        self.assertEqual(Building.get_construction(Building, 2), None)
        self.assertEqual(Building.get_construction(Building, 3), Building.DoesNotExist)

    def test22_get_material(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_material(Building, 0), '')
        self.assertEqual(Building.get_material(Building, 1), 'penetelischer Marmor')
        self.assertEqual(Building.get_material(Building, 2), None)
        self.assertEqual(Building.get_material(Building, 3), Building.DoesNotExist)

    def test23_get_literature(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_literature(Building, 0), '')
        self.assertEqual(Building.get_literature(Building, 1),
                         'Muss - Schubert 1988, SEITEN?; Gruben 2001, 173-190; Hellmann 2006, '
                         '82-96;')
        self.assertEqual(Building.get_literature(Building, 2), None)
        self.assertEqual(Building.get_literature(Building, 3), Building.DoesNotExist)

    def test24_get_description(self):
        """
        Testing get_description
        """
        self.assertEqual(Building.get_description(Building, 0), '')
        self.assertEqual(Building.get_description(Building, 1), 'Das Parthenon in Athen')
        self.assertEqual(Building.get_description(Building, 2), None)
        self.assertEqual(Building.get_description(Building, 3), Building.DoesNotExist)

    def test25_get_year_ca(self):
        """
        Testing get_year_ca
        """
        self.assertEqual(Building.get_year_ca(Building, 0), False)
        self.assertEqual(Building.get_year_ca(Building, 1), True)
        self.assertEqual(Building.get_year_ca(Building, 2), False)
        self.assertEqual(Building.get_year_ca(Building, 3), Building.DoesNotExist)

    def test26__str__(self):
        """
        Testing the __str__ function
        """
        test1 = Building.objects.get(name='').__str__()
        test2 = Building.objects.get(name='Parthenon').__str__()
        self.assertEqual(test1, '')
        self.assertEqual(test2, 'Parthenon')

    def test27_get_links(self):
        """
        Testing get_name
        """
        self.assertEqual(Building.get_links(Building, 0), list(''))
        self.assertEqual(Building.get_links(Building, 1), ["www.tu-darmstadt.de",
                                                           "www.architektur.tu-darmstadt.de"])
        self.assertEqual(Building.get_links(Building, 2), list(''))
        self.assertEqual(Building.get_links(Building, 3), Building.DoesNotExist)


class EraModelTests(TestCase):
    """
    Tests for Era Model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Setup for test data
        :return: None
        """
        cls.testera = Era.objects.create(name="Frühzeit", year_from=1, year_from_BC_or_AD="",
                                         year_to=1,
                                         year_to_BC_or_AD="", visible_on_video_page=True,
                                         color_code="ffffff")

    def test_response(self):
        """
        Simple response and get tests on object
        :return: None / Test results
        """
        self.assertEqual(Era.objects.get(pk=1), self.testera)
        self.assertEqual(Era.objects.get(pk=1).name, self.testera.name)
        self.assertEqual(Era.objects.get(pk=1).year_from, self.testera.year_from)
        self.assertEqual(Era.objects.get(pk=1).year_from_BC_or_AD, self.testera.year_from_BC_or_AD)
        self.assertEqual(Era.objects.get(pk=1).year_to, self.testera.year_to)
        self.assertEqual(Era.objects.get(pk=1).year_to_BC_or_AD, self.testera.year_to_BC_or_AD)
        self.assertEqual(Era.objects.get(pk=1).visible_on_video_page,
                         self.testera.visible_on_video_page)
        self.assertEqual(Era.objects.get(pk=1).color_code, self.testera.color_code)

    def test__str__(self):
        era = Era.objects.create(name="Archaik", year_from=1, year_from_BC_or_AD="", year_to=1,
                                 year_to_BC_or_AD="",
                                 visible_on_video_page=True, color_code="fffff")
        self.assertEqual(str(Era.objects.get(pk=1)), self.testera.name)
        self.assertEqual(str(Era.objects.get(pk=2)), era.name)


class PictureTests(TestCase):
    """
    Tests for Picture Model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Setup for test data
        :return: None
        """
        cls.client = Client()
        cls.test_era = Era.objects.create(name='Frühe Kaiserzeit', year_from=55,
                                          year_from_BC_or_AD='v.Chr', year_to=55,
                                          year_to_BC_or_AD='v.Chr')
        cls.test_building_1 = Building.objects.create(pk=0, name='', description='', city='',
                                                      region='',
                                                      country='', year_from=0,
                                                      year_from_BC_or_AD='',
                                                      year_to=0, year_to_BC_or_AD='',
                                                      year_ca=False,
                                                      era=cls.test_era,
                                                      architect='', context='', builder='',
                                                      construction_type='', design='', function='',
                                                      length=0, width=0, height=0,
                                                      circumference=0, area=0, column_order='',
                                                      construction='', material='',
                                                      literature='')
        cls.test_building_2 = Building.objects.create(pk=1, name='Parthenon',
                                                      description='Das Parthenon in Athen',
                                                      city='Athen',
                                                      region='TestRegion',
                                                      country='GR-Griechenland',
                                                      year_from=447, year_from_BC_or_AD='v.Chr.',
                                                      year_to=438, year_to_BC_or_AD='v.Chr.',
                                                      year_ca=True,
                                                      era=cls.test_era,
                                                      architect='Iktinos, Kallikrates',
                                                      context='Tempel',
                                                      builder='Perikles und die Polis Athen',
                                                      construction_type='Tempel',
                                                      design='Peripteros', function='Sakralbau',
                                                      length=30.88, width=69.5, height=1,
                                                      circumference=1, area=1,
                                                      column_order='dorisch, ionischer Fries',
                                                      construction='Massivbau',
                                                      material='penetelischer Marmor',
                                                      literature='Muss - Schubert 1988, SEITEN?; '
                                                                 'Gruben 2001, 173-190; Hellmann '
                                                                 '2006, 82-96;')
        cls.p = Picture.objects.create(name='', picture=image_mock,
                                       building=cls.test_building_1, usable_as_thumbnail=False)
        cls.p2 = Picture.objects.create(name='', picture=image_mock2,
                                        building=cls.test_building_2, usable_as_thumbnail=False)

    def test_response(self):
        """
        Simple get tests for picture.
        :return: None / test results
        """
        self.assertEqual(Picture.objects.get(pk=1), self.p)
        self.assertEqual(Picture.objects.get(pk=1).name, self.p.name)
        self.assertEqual(Picture.objects.get(pk=1).picture, self.p.picture)
        self.assertEqual(Picture.objects.get(pk=1).building, self.test_building_1)
        self.assertEqual(Picture.objects.get(pk=1).usable_as_thumbnail, self.p.usable_as_thumbnail)

    def test_response_p2(self):
        """
        Simple get tests for picture.
        :return: None / test results
        """
        self.assertEqual(Picture.objects.get(pk=2), self.p2)
        self.assertEqual(Picture.objects.get(pk=2).name, self.p2.name)
        self.assertEqual(Picture.objects.get(pk=2).picture, self.p2.picture)
        self.assertEqual(Picture.objects.get(pk=2).building, self.test_building_2)
        self.assertEqual(Picture.objects.get(pk=2).usable_as_thumbnail, self.p2.usable_as_thumbnail)

    def test__str__(self):
        """
        Simple Name Test for __str__() method
        :return:
        """
        self.assertEqual(str(Picture.objects.get(pk=1)), self.p.name)
        self.assertEqual(str(Picture.objects.get(pk=2)), self.p2.name)


class BlueprintTests(TestCase):
    """
    Test for Blueprint Model
    """

    def setUp(self):
        """
        Setting up objects and a client for the tests
        """
        self.client = Client()
        self.test_era = Era.objects.create(name='Frühe Kaiserzeit', year_from=55,
                                           year_from_BC_or_AD='v.Chr', year_to=55,
                                           year_to_BC_or_AD='v.Chr')
        self.test_building_1 = Building.objects.create(pk=0, name='', description='', city='',
                                                       region='',
                                                       country='', year_from=0,
                                                       year_from_BC_or_AD='',
                                                       year_to=0, year_to_BC_or_AD='',
                                                       year_ca=False,
                                                       era=self.test_era,
                                                       architect='', context='', builder='',
                                                       construction_type='', design='', function='',
                                                       length=0, width=0, height=0,
                                                       circumference=0, area=0, column_order='',
                                                       construction='', material='',
                                                       literature='')
        self.test_building_2 = Building.objects.create(pk=1, name='Parthenon',
                                                       description='Das Parthenon in Athen',
                                                       city='Athen',
                                                       region='TestRegion',
                                                       country='GR-Griechenland',
                                                       year_from=447, year_from_BC_or_AD='v.Chr.',
                                                       year_to=438, year_to_BC_or_AD='v.Chr.',
                                                       year_ca=True,
                                                       era=self.test_era,
                                                       architect='Iktinos, Kallikrates',
                                                       context='Tempel',
                                                       builder='Perikles und die Polis Athen',
                                                       construction_type='Tempel',
                                                       design='Peripteros', function='Sakralbau',
                                                       length=30.88, width=69.5, height=1,
                                                       circumference=1, area=1,
                                                       column_order='dorisch, ionischer Fries',
                                                       construction='Massivbau',
                                                       material='penetelischer Marmor',
                                                       literature='Muss - Schubert 1988, '
                                                                  'SEITEN?; Gruben 2001, 173-190; '
                                                                  'Hellmann 2006, 82-96;')
        self.bp1 = Blueprint.objects.create(name='', blueprint=image_mock, width=0,
                                            height=0,
                                            building=self.test_building_1)
        self.bp2 = Blueprint.objects.create(name='TestBlueprint1', blueprint=image_mock2,
                                            width=10, height=10,
                                            building=self.test_building_2)

    def test1__str__(self):
        """
        Testing the __str__ function
        """
        test1 = Blueprint.objects.get(name='').__str__()
        test2 = Blueprint.objects.get(name='TestBlueprint1').__str__()
        self.assertEqual(test1, '')
        self.assertEqual(test2, 'TestBlueprint1')

    def test2_get_blueprint_for_building(self):
        """
        Testing the get_blueprint_for_building function
        """
        self.assertEqual(list(Blueprint.get_blueprint_for_building(Blueprint, 1)),
                         list(Blueprint.objects.filter(pk=2)))
        self.assertEqual(list(Blueprint.get_blueprint_for_building(Blueprint, 0)),
                         list(Blueprint.objects.filter(pk=1)))
        self.assertEqual(list(Blueprint.get_blueprint_for_building(Blueprint, 3)),
                         list(Blueprint.objects.filter(pk=3)))


class ModelFunctionTests(TestCase):
    """
    Testing the function oustide of the classes in details_page.models
    """

    def setUp(self):
        """
        Setting up some TestData
        """
        self.era1 = Era(name="Archaik", year_from=700, year_from_BC_or_AD="v.Chr.", year_to=500,
                        year_to_BC_or_AD="v.Chr.",
                        visible_on_video_page=True, color_code="fffff")
        self.era2 = Era(name='Klassik', year_from_BC_or_AD='v.Chr.', year_to=337,
                        year_to_BC_or_AD='v.Chr.')
        self.era3 = Era(name='Frühzeit')
        self.building1 = Building(name='Baum in Ganeshas Garten', year_from=100, year_to=50,
                                  year_from_BC_or_AD='v.Chr.', year_to_BC_or_AD='n.Chr.')
        self.building2 = Building(name='Baum in Jonathans Garten', year_from=700,
                                  year_from_BC_or_AD='v.Chr.', year_to_BC_or_AD='v.Chr.')
        self.building3 = Building(name='Nichts')
        self.building4 = Building(name='Century', year_from=3, year_to=1, year_century=True,
                                  year_from_BC_or_AD='v.Chr.', year_to_BC_or_AD='n.Chr.')

    def test_validator_color_code(self):
        """
        Test the validators for color codes.
        :return: None / Test results
        """
        string1 = ''
        string2 = 'zzzzzz'
        string3 = 'AbCdEf'
        string4 = '111111111111111'
        string5 = '01A3f5'

        # Testing with empty string
        self.assertRaises(ValidationError, validate_color_code, string1)
        self.assertRaisesMessage(ValidationError, "['Bitte einen gültigen Code im Hex-Format "
                                                  "einfügen: Muss genau 6 Zeichen lang sein.']")

        # Testing with non-hex-characters
        self.assertRaises(ValidationError, validate_color_code, string2)
        self.assertRaisesMessage(ValidationError,
                                 "['Bitte einen gültigen Code im Hex-Format "
                                 "einfügen: Nur Hex-Zeichen: 0-9, a-f und A-F.']",
                                 validate_color_code, string2)

        # Testing with to long string
        self.assertRaises(ValidationError, validate_color_code, string4)
        self.assertRaisesMessage(ValidationError,
                                 "['Bitte einen gültigen Code im Hex-Format "
                                 "einfügen: Muss genau 6 Zeichen lang sein.']",
                                 validate_color_code, string4)

        # Testing with two correct strings
        self.assertEqual(validate_color_code(string3), None)
        self.assertEqual(validate_color_code(string5), None)

    def test_validate_url_conform_str(self):
        """
        Testing validate_url_conform_str
        """
        string1 = 'Baum in Ganeshas Garten'
        string2 = 'Baum+in+Ganeshas+Garten'
        string3 = 'Baum,in,Ganeshas,Garten.'
        string4 = 'B+a.u,m:i-n%!Gan€shas#$=9873)}[]``´´§Garten<>|_^°*~@'
        string5 = 'Baum in Ganeshas Garten?'
        string6 = 'Baum/in\'Ganeshas\'"Garten@-+#&'
        # Testing with legal strings
        self.assertEqual(validate_url_conform_str(string1), None)
        self.assertEqual(validate_url_conform_str(string2), None)
        self.assertEqual(validate_url_conform_str(string3), None)
        self.assertEqual(validate_url_conform_str(string4), None)

        # Testing with illegal strings
        self.assertRaises(ValidationError, validate_url_conform_str, string5)
        self.assertRaises(ValidationError, validate_url_conform_str, string6)

    def test_get_year_as_signed_int(self):
        """
        Testing the get_year_as_signed_int function
        """
        # Testing era with no empty fields
        self.assertEqual(get_year_as_signed_int(self.era1), [-700, -500])

        # Testing era with one empty field
        self.assertEqual(get_year_as_signed_int(self.era2), [9999, -337])

        # Testing era with only a name
        self.assertEqual(get_year_as_signed_int(self.era3),
                         [9999, 9999])

        # Testing building with no empty fields
        self.assertEqual(get_year_as_signed_int(self.building1), [-100, 50])

        # Testing building with one empty field
        self.assertEqual(get_year_as_signed_int(self.building2), [-700, 9999])

        # Testing building with only a name
        self.assertEqual(get_year_as_signed_int(self.building3),
                         [9999, 9999])

        # Testing Century
        self.assertEqual(get_year_as_signed_int(self.building4), [-250, 50])
