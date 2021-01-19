"""
Tests for the functions in the App: details_page
"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from details_page.models import Era, Picture, Building


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
        cls.testera = Era.objects.create(name="Frühzeit", year_from=1, year_from_BC_or_AD="", year_to=1, year_to_BC_or_AD="",
                                         visible_on_video_page=True, color_code="ffffff")

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
        self.assertEqual(Era.objects.get(pk=1).visible_on_video_page, self.testera.visible_on_video_page)
        self.assertEqual(Era.objects.get(pk=1).color_code, self.testera.color_code)

    def test_validator(self):
        """
        Test the validators for Era.
        :return: None / Test results
        """
        era = Era(name="Archaik", year_from=1, year_from_BC_or_AD="", year_to=1,
                  year_to_BC_or_AD="",
                  visible_on_video_page=True, color_code="fffff")
        self.assertRaises(ValidationError, era.full_clean)
        self.assertRaisesMessage(ValidationError, "{'color_code': ['Bitte einen gültigen Code im Hex-Format einfügen: "
                                                  "Muss genau 6 Zeichen lang sein.']}", era.full_clean)
        era.color_code = "zzzzzz"
        self.assertRaises(ValidationError, era.full_clean)
        self.assertRaisesMessage(ValidationError, "{'color_code': ['Bitte einen gültigen Code im Hex-Format einfügen: "
                                                  "Nur Hex-Zeichen: 0-9, a-f und A-F.']}", era.full_clean)

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
        cls.b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        cls.p = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                       building=cls.b, usable_as_thumbnail=False)
        cls.p2 = Picture.objects.create(name="Test2", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                        building=cls.b, usable_as_thumbnail=False)

    def test_response(self):
        """
        Simple get tests for picture.
        :return: None / test results
        """
        self.assertEqual(Picture.objects.get(pk=1), self.p)
        self.assertEqual(Picture.objects.get(pk=1).name, self.p.name)
        self.assertEqual(Picture.objects.get(pk=1).picture, self.p.picture)
        self.assertEqual(Picture.objects.get(pk=1).building, self.b)
        self.assertEqual(Picture.objects.get(pk=1).usable_as_thumbnail, self.p.usable_as_thumbnail)

    def test__str__(self):
        """
        Simple Name Test for __str__() method
        :return:
        """
        self.assertEqual(str(Picture.objects.get(pk=1)), self.p.name)
        self.assertEqual(str(Picture.objects.get(pk=2)), self.p2.name)
