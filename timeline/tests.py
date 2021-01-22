"""
Tests for functions in the App: timeline
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from datetime import date
from timeline.models import HistoricDate
from details_page.models import Era, Building, Picture
from timeline.views import get_date_as_str


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
        Testing timeline function in views
        """
        response = self.client.get('/timeline/')
        self.assertEqual(response.status_code, 200)


class HistoricDatesModelTests(TestCase):
    """
    Tests for the HistoricDate Model in timeline/models.py
    """

    @classmethod
    def setUpTestData(cls):
        """
        Setup Testdate that is used for every test method.
        We need an Era to give to the foreign key in HistoricDate, for testing.
        :return: None
        """
        cls.an_era = Era.objects.create(name="Testepoche", year_from=10, year_from_BC_or_AD="v.Chr.", year_to=100,
                                        year_to_BC_or_AD="n.Chr.", visible_on_video_page=True, color_code="ffffff")
        cls.client = Client()

    def test_get_empty(self):
        """
        Test for get all objects when nothing was added
        :return: None / Test results
        """
        self.assertListEqual(list(HistoricDate.objects.all()), [])

    def test_response_for_timeline_url(self):
        response = self.client.get('/timeline/')
        self.assertEqual(response.status_code, 200)

    def test_entries_correct(self):
        """
        Test the entries if correct data was given
        :return: None / Test results
        """
        hd = HistoricDate.objects.create(year=17, exacter_date=None, year_BC_or_AD="n.Chr.",
                                         title="Test Datum", infos="Ein Test Datum", era=self.an_era)
        self.assertEqual(HistoricDate.objects.get(title="Test Datum"), hd)
        self.assertEqual(HistoricDate.objects.get(pk=1).year, hd.year)
        self.assertEqual(HistoricDate.objects.get(pk=1).exacter_date, hd.exacter_date)
        self.assertEqual(HistoricDate.objects.get(pk=1).year_BC_or_AD, hd.year_BC_or_AD)
        self.assertEqual(HistoricDate.objects.get(pk=1).title, hd.title)
        self.assertEqual(HistoricDate.objects.get(pk=1).infos, hd.infos)
        self.assertEqual(HistoricDate.objects.get(pk=1).era, hd.era)

    def test_validation_errors(self):
        """
        Test for validations errors to be raised, if input was not valid
        :return: None / Test results
        """

        hd = HistoricDate.objects.create(year=0, exacter_date=None,
                                         year_BC_or_AD="n.Chr.",
                                         title="Test Datum",
                                         infos="Ein Test Datum",
                                         era=self.an_era)

        # If year number is too high
        hd.year = max_year + 100
        self.assertRaises(ValidationError, hd.full_clean)
        self.assertRaisesMessage(ValidationError,
                                 "{'year': ['Diese Jahreszahl ist zu hoch. Bitte etwas zwischen 0 und "
                                 + str(max_year)
                                 + " eingeben.']}",
                                 hd.full_clean)

        # If date is too high
        hd.year = max_year - 1
        hd.exacter_date = date(max_year + 1, 1, 1)
        self.assertRaises(ValidationError, hd.full_clean)
        self.assertRaisesMessage(ValidationError,
                                 "{'exacter_date': ['Das eingegebene Datum ist zu hoch. Bitte etwas zwischen "
                                 + "dem 01.01.0000 und dem 31.12."
                                 + str(max_year)
                                 + " eingeben.']}",
                                 hd.full_clean)

    def test__str__(self):
        """
        Tests for the __str__ method of the model
        :return: None / Test results
        """
        # for just a year number
        hd = HistoricDate.objects.create(year=23, exacter_date=None,
                                         year_BC_or_AD="n.Chr.",
                                         title="Test",
                                         infos="Ein Test Datum",
                                         era=self.an_era)
        self.assertEqual(str(HistoricDate.objects.get(title="Test")), str(hd.title) + " (" + str(hd.year) + " "
                         + str(hd.year_BC_or_AD) + ")")
        # with exacter date
        hd.exacter_date = date(23, 3, 1)
        hd.save()
        self.assertEqual(str(HistoricDate.objects.get(title="Test")), str(hd.title) + " (" + str(hd.exacter_date)
                         + " " + str(hd.year_BC_or_AD) + ")")


class TimelineViewsTest(TestCase):
    """
    Tests for the views.py for the timeline app.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Setup the test Data for every test
        :return: None
        """
        cls.client = Client()
        cls.bronzezeit = Era.objects.create(name="Bronzezeit", year_from=1400, year_from_BC_or_AD="v.Chr.",
                                            year_to=1101,
                                            year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff1")
        cls.eisenzeit = Era.objects.create(name="Eisenzeit", year_from=1100, year_from_BC_or_AD="v.Chr.", year_to=701,
                                           year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff2")
        cls.archaik = Era.objects.create(name="Arachik", year_from=700, year_from_BC_or_AD="v.Chr.", year_to=501,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff3")
        cls.klassik = Era.objects.create(name="Klassisk", year_from=500, year_from_BC_or_AD="v.Chr.", year_to=337,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff4")
        cls.helinismus = Era.objects.create(name="Helinismus", year_from=336, year_from_BC_or_AD="v.Chr.", year_to=100,
                                            year_to_BC_or_AD="n.Chr.", visible_on_video_page=True, color_code="fffff5")

    def test_timeline_empty(self):
        """
        Test for get all timeline itmes and thumbnails when nothing was added
        :return: None / Test results
        """
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [])
        self.assertEqual(response.context["thumbnails"], {})

    def setup_some(self):
        """
        Just a simple setup for some test data.
        :return: All these Buildings and HistoricDates defined beneath
        """
        b1 = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        b2 = Building.objects.create(name="Building 2", date_from=5, date_from_BC_or_AD="v.Chr.")
        b3 = Building.objects.create(name="Building 3", date_from=10, date_from_BC_or_AD="n.Chr.")
        b4 = Building.objects.create(name="Building 4", date_from=100, date_from_BC_or_AD="n.Chr.")
        hd1 = HistoricDate.objects.create(year=50, exacter_date=None,
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.bronzezeit)
        hd2 = HistoricDate.objects.create(year=0, exacter_date=None,
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 2",
                                          infos="Ein Test Datum",
                                          era=self.eisenzeit)
        hd3 = HistoricDate.objects.create(year=0, exacter_date=None,
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.archaik)
        hd4 = HistoricDate.objects.create(year=50, exacter_date=None,
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.klassik)
        return b1, b2, b3, b4, hd1, hd2, hd3, hd4

    def test_timeline_with_year(self):
        """
        Tests for timeline view, with year numbers
        :return: None / Test results
        """
        b1, b2, b3, b4, hd1, hd2, hd3, hd4 = self.setup_some()
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b1, hd1, b2, hd2, hd3, b3, hd4, b4])
        self.assertEqual(response.context["thumbnails"], {1: None, 2: None, 3: None, 4: None})

    def test_timeline_with_year_add(self):
        """
        Tests for timeline view, with year numbers, more complex
        :return: None / Test results
        """
        b1, b2, b3, b4, hd1, hd2, hd3, hd4 = self.setup_some()
        b5 = Building.objects.create(name="Building 5", date_from=4, date_from_BC_or_AD="v.Chr.")
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b1, hd1, b2, b5, hd2, hd3, b3, hd4, b4])
        self.assertEqual(response.context["thumbnails"], {1: None, 2: None, 3: None, 4: None, 5: None})

    def test_timeline_without_year_sorting(self):
        """
        Tests for timeline view, with and without year numbers, more complex
        :return: None / Test results
        """
        b1, b2, b3, b4, hd1, hd2, hd3, hd4 = self.setup_some()
        b3.date_from = None
        b3.save()
        b5 = Building.objects.create(name="Building 5", date_from=4, date_from_BC_or_AD="v.Chr.")
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b1, hd1, b2, b5, hd2, hd3, hd4, b4])
        self.assertEqual(response.context["thumbnails"], {1: None, 2: None, 4: None, 5: None})

    def setup_some2(self):
        """
        Simple Setup for some test data
        :return: None
        """
        b1 = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        b2 = Building.objects.create(name="Building 2", date_from=5, date_from_BC_or_AD="v.Chr.")
        b3 = Building.objects.create(name="Building 3", date_from=10, date_from_BC_or_AD="n.Chr.")
        b4 = Building.objects.create(name="Building 4", date_from=100, date_from_BC_or_AD="n.Chr.")
        hd1 = HistoricDate.objects.create(year=50, exacter_date=date(50, 1, 1),
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.bronzezeit)
        hd2 = HistoricDate.objects.create(year=1, exacter_date=date(1, 3, 1),
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 2",
                                          infos="Ein Test Datum",
                                          era=self.eisenzeit)
        hd3 = HistoricDate.objects.create(year=1, exacter_date=date(1, 1, 5),
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.archaik)
        hd4 = HistoricDate.objects.create(year=50, exacter_date=date(50, 5, 8),
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.klassik)
        return b1, b2, b3, b4, hd1, hd2, hd3, hd4

    def test_timeline_with_date(self):
        """
        Tests for timeline view, with actual dates
        :return: None / Test results
        """
        b1, b2, b3, b4, hd1, hd2, hd3, hd4 = self.setup_some2()
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b1, hd1, b2, hd2, hd3, b3, hd4, b4])
        self.assertEqual(response.context["thumbnails"], {1: None, 2: None, 3: None, 4: None})

    def test_timeline_with_mixed(self):
        """
        Tests for timeline view, with year numbers and dates, more complex
        :return: None / Test results
        """
        b1, b2, b3, b4, hd1, hd2, hd3, hd4 = self.setup_some2()
        b3.exacter_date = None
        b3.save()
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b1, hd1, b2, hd2, hd3, b3, hd4, b4])
        self.assertEqual(response.context["thumbnails"], {1: None, 2: None, 3: None, 4: None})

    def test_timeline_with_date_add(self):
        """
        Tests for timeline view, with dates, more complex
        :return: None / Test results
        """
        b1, b2, b3, b4, hd1, hd2, hd3, hd4 = self.setup_some2()
        b5 = Building.objects.create(name="Building 5", date_from=4, date_from_BC_or_AD="v.Chr.")
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b1, hd1, b2, b5, hd2, hd3, b3, hd4, b4])
        self.assertEqual(response.context["thumbnails"], {1: None, 2: None, 3: None, 4: None, 5: None})

    def test_timeline_with_date_without_year_sorting(self):
        """
        Tests for timeline view, with dates and without year numbers, more complex
        :return: None / Test results
        """
        b1, b2, b3, b4, hd1, hd2, hd3, hd4 = self.setup_some2()
        b3.date_from = None
        b3.save()
        b5 = Building.objects.create(name="Building 5", date_from=4, date_from_BC_or_AD="v.Chr.")
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b1, hd1, b2, b5, hd2, hd3, hd4, b4])
        self.assertEqual(response.context["thumbnails"], {1: None, 2: None, 4: None, 5: None})

    def test_thumbnail_empty(self):
        """
        Tests for thumbnail assignment and sorting: empty thumbnails
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b])
        self.assertEqual(response.context["thumbnails"], {1: None})

    def test_thumbnail_disabled(self):
        """
        Tests for thumbnail assignment and sorting: thumbnail, but not assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        p = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                   building=b, usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b])
        self.assertEqual(response.context["thumbnails"], {1: None})

    def test_thumbnail_enabled(self):
        """
        Tests for thumbnail assignment and sorting: thumbnail, assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        p = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                   building=b, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b])
        self.assertEqual(response.context["thumbnails"], {1: p})

    def test_thumbnail_more_disabled(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, all not assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        p1 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=False)
        p2 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b])
        self.assertEqual(response.context["thumbnails"], {1: None})

    def test_thumbnail_more_both1(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, one assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        p1 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=True)
        p2 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b])
        self.assertEqual(response.context["thumbnails"], {1: p1})

    def test_thumbnail_more_both2(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, one other assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        p1 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=False)
        p2 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b])
        self.assertEqual(response.context["thumbnails"], {1: p2})

    def test_thumbnail_more_enabled(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, all assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        p1 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=True)
        p2 = Picture.objects.create(name="Test", picture="../media/pics/external-content.duckduckgo.com.jpg",
                                    building=b, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items"], [b])
        # thumbnail will be chosen random, so it is one of either (in this list)
        self.assertIn(response.context["thumbnails"], [{1: p1}, {1: p2}])


class GetDateAsStingTests(TestCase):
    """
    Tests for class method get_date_as_string(item), witch returns the date in best manner, as Sting.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Just a simple setup for some test data.
        :return: All these Buildings and HistoricDates defined beneath
        """
        cls.client = Client()
        cls.bronzezeit = Era.objects.create(name="Bronzezeit", year_from=1400, year_from_BC_or_AD="v.Chr.",
                                            year_to=1101,
                                            year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff1")
        cls.eisenzeit = Era.objects.create(name="Eisenzeit", year_from=1100, year_from_BC_or_AD="v.Chr.", year_to=701,
                                           year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff2")
        cls.archaik = Era.objects.create(name="Arachik", year_from=700, year_from_BC_or_AD="v.Chr.", year_to=501,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff3")
        cls.klassik = Era.objects.create(name="Klassisk", year_from=500, year_from_BC_or_AD="v.Chr.", year_to=337,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True, color_code="fffff4")
        cls.helinismus = Era.objects.create(name="Helinismus", year_from=336, year_from_BC_or_AD="v.Chr.", year_to=100,
                                            year_to_BC_or_AD="n.Chr.", visible_on_video_page=True, color_code="fffff5")
        cls.b1 = Building.objects.create(name="Building 1", date_from=100, date_from_BC_or_AD="v.Chr.")
        cls.b2 = Building.objects.create(name="Building 2", date_from=5, date_from_BC_or_AD="v.Chr.")
        cls.b3 = Building.objects.create(name="Building 3", date_from=10, date_from_BC_or_AD="n.Chr.")
        cls.b4 = Building.objects.create(name="Building 4", date_from=100, date_from_BC_or_AD="n.Chr.")
        cls.hd1 = HistoricDate.objects.create(year=50, exacter_date=date(50, 3, 27),
                                              year_BC_or_AD="v.Chr.",
                                              title="Historic Date 1",
                                              infos="Ein Test Datum",
                                              era=cls.bronzezeit)
        cls.hd2 = HistoricDate.objects.create(year=0, exacter_date=date(1, 1, 1),
                                              year_BC_or_AD="v.Chr.",
                                              title="Historic Date 2",
                                              infos="Ein Test Datum",
                                              era=cls.eisenzeit)
        cls.hd3 = HistoricDate.objects.create(year=0, exacter_date=None,
                                              year_BC_or_AD="n.Chr.",
                                              title="Historic Date 1",
                                              infos="Ein Test Datum",
                                              era=cls.archaik)
        cls.hd4 = HistoricDate.objects.create(year=50, exacter_date=date(50, 7, 8),
                                              year_BC_or_AD="n.Chr.",
                                              title="Historic Date 1",
                                              infos="Ein Test Datum",
                                              era=cls.klassik)

    def test_getDates(self):
        """
        Test the date result as str. Caution: Tests run with locale="en-EN",
        Date-Format is other than it might be in german environment!
        :return: None / Test results
        """
        self.assertEqual(get_date_as_str(self.b1), "100 v.Chr.")
        self.assertEqual(get_date_as_str(self.b2), "5 v.Chr.")
        self.assertEqual(get_date_as_str(self.b3), "10 n.Chr.")
        self.assertEqual(get_date_as_str(self.b4), "100 n.Chr.")
        self.assertEqual(get_date_as_str(self.hd1), "0050-03-27 v.Chr.")
        self.assertEqual(get_date_as_str(self.hd2), "0001-01-01 v.Chr.")
        self.assertEqual(get_date_as_str(self.hd3), "0 n.Chr.")
        self.assertEqual(get_date_as_str(self.hd4), "0050-07-08 n.Chr.")
