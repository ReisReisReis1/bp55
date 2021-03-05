"""
Tests for functions in the App: timeline
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from datetime import date
from timeline.models import HistoricDate
from details_page.models import Era, Building, Picture
from timeline.views import get_date_as_str, get_start_year_of_item

# Define some temp images for testing
thumbnail_default = None
test_image = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
              b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
              b'\x02\x4c\x01\x00\x3b')
image_mock = SimpleUploadedFile('small.img', test_image, content_type='image/gif')
image_mock2 = SimpleUploadedFile('small.img', test_image, content_type='image/gif')


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
        cls.an_era = Era.objects.create(name="Testepoche", year_from=10,
                                        year_from_BC_or_AD="v.Chr.", year_to=100,
                                        year_to_BC_or_AD="n.Chr.", visible_on_video_page=True,
                                        color_code="ffffff")
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
                                         title="Test Datum", infos="Ein Test Datum",
                                         era=self.an_era)
        self.assertEqual(HistoricDate.objects.get(title="Test Datum"), hd)
        self.assertEqual(HistoricDate.objects.get(pk=1).year, hd.year)
        self.assertEqual(HistoricDate.objects.get(pk=1).exacter_date, hd.exacter_date)
        self.assertEqual(HistoricDate.objects.get(pk=1).year_BC_or_AD, hd.year_BC_or_AD)
        self.assertEqual(HistoricDate.objects.get(pk=1).title, hd.title)
        self.assertEqual(HistoricDate.objects.get(pk=1).infos, hd.infos)
        self.assertEqual(HistoricDate.objects.get(pk=1).era, hd.era)

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
        self.assertEqual(str(HistoricDate.objects.get(title="Test")), str(hd.title)
                         + " (" + str(hd.year) + " "
                         + str(hd.year_BC_or_AD) + ")")
        # with exacter date
        hd.exacter_date = date(23, 3, 1)
        hd.save()
        self.assertEqual(str(HistoricDate.objects.get(title="Test")), str(hd.title)
                         + " (" + '1.3.23 n.Chr.' + ")")

    def test_get_year_as_signed_int(self):
        """
        Testing the function get_year_as_signed_int in the historic date
        """
        # Getting the default year
        h1 = HistoricDate.objects.create()
        self.assertEqual(h1.get_year_as_signed_int(), 9999)

        # Exact date
        h2 = HistoricDate.objects.create(exacter_date=date(2, 1, 1), year_BC_or_AD="n.Chr.")
        self.assertEqual(h2.get_year_as_signed_int(), 2)

        # Year
        h3 = HistoricDate.objects.create(year=100, year_BC_or_AD="v.Chr.")
        h4 = HistoricDate.objects.create(year=100, year_BC_or_AD="n.Chr.")
        self.assertEqual(h3.get_year_as_signed_int(), -100)
        self.assertEqual(h4.get_year_as_signed_int(), 100)

        # Both exists
        h5 = HistoricDate.objects.create(year=100, year_BC_or_AD="v.Chr.",
                                         exacter_date=date(1, 2, 3))
        self.assertEqual(h5.get_year_as_signed_int(), -1)

        # Year century
        h6 = HistoricDate.objects.create(year=1, year_BC_or_AD='v.Chr.', year_century=True)
        h7 = HistoricDate.objects.create(year=1, year_BC_or_AD='n.Chr.', year_century=True)
        self.assertEqual(h6.get_year_as_signed_int(), -50)
        self.assertEqual(h7.get_year_as_signed_int(), 50)


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

        cls.bronzezeit = Era.objects.create(name="Bronzezeit", year_from=1400,
                                            year_from_BC_or_AD="v.Chr.",
                                            year_to=1100,
                                            year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                            color_code="fffff1")
        cls.frühzeit = Era.objects.create(name="Frühzeit", year_from=1100,
                                          year_from_BC_or_AD="v.Chr.", year_to=700,
                                          year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                          color_code="fffff2")
        cls.archaik = Era.objects.create(name="Archaik", year_from=700, year_from_BC_or_AD="v.Chr.",
                                         year_to=500,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                         color_code="fffff3")
        cls.klassik = Era.objects.create(name="Klassik", year_from=500,
                                         year_from_BC_or_AD="v.Chr.", year_to=337,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                         color_code="fffff4")
        cls.hellenismus = Era.objects.create(name="Hellenismus", year_from=337,
                                             year_from_BC_or_AD="v.Chr.", year_to=30,
                                             year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                             color_code="fffff5")
        cls.kaiserzeit = Era.objects.create(name='Kaiserzeit', year_from=30,
                                            year_from_BC_or_AD='n.Chr.', year_to=284,
                                            year_to_BC_or_AD='n.Chr.',
                                            visible_on_video_page=True)
        cls.spätantike = Era.objects.create(name='Spätantike', year_from=284,
                                            year_from_BC_or_AD='n.Chr.', year_to=565,
                                            year_to_BC_or_AD='n.Chr.', visible_on_video_page=True)

    def test_timeline_empty(self):
        """
        Test for get all timeline items and thumbnails when nothing was added
        :return: None / Test results
        """
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, []),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])})

    def setup_some(self):
        """
        Just a simple setup for some test data.
        :return: All these Buildings and HistoricDates defined beneath
        """
        b1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        b2 = Building.objects.create(name="Building 2", year_from=5, year_from_BC_or_AD="v.Chr.")
        b3 = Building.objects.create(name="Building 3", year_from=10, year_from_BC_or_AD="n.Chr.")
        b4 = Building.objects.create(name="Building 4", year_from=100, year_from_BC_or_AD="n.Chr.")

        hd1 = HistoricDate.objects.create(year=50, exacter_date=None,
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.bronzezeit)
        hd2 = HistoricDate.objects.create(year=0, exacter_date=None,
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 2",
                                          infos="Ein Test Datum",
                                          era=self.frühzeit)
        hd3 = HistoricDate.objects.create(year=0, exacter_date=None,
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 3",
                                          infos="Ein Test Datum",
                                          era=self.archaik)
        hd4 = HistoricDate.objects.create(year=50, exacter_date=None,
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 4",
                                          infos="Ein Test Datum",
                                          era=self.klassik)
        return b1, b2, b3, b4, hd1, hd2, hd3, hd4

    def setup_some2(self):
        """
        Simple Setup for some test data
        :return: None
        """
        b1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        b2 = Building.objects.create(name="Building 2", year_from=5, year_from_BC_or_AD="v.Chr.")
        b3 = Building.objects.create(name="Building 3", year_from=10, year_from_BC_or_AD="n.Chr.")
        b4 = Building.objects.create(name="Building 4", year_from=100, year_from_BC_or_AD="n.Chr.")
        hd1 = HistoricDate.objects.create(year=50, exacter_date=date(50, 1, 1),
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=self.bronzezeit)
        hd2 = HistoricDate.objects.create(year=1, exacter_date=date(1, 3, 1),
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 2",
                                          infos="Ein Test Datum",
                                          era=self.frühzeit)
        hd3 = HistoricDate.objects.create(year=1, exacter_date=date(1, 1, 5),
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 3",
                                          infos="Ein Test Datum",
                                          era=self.archaik)
        hd4 = HistoricDate.objects.create(year=50, exacter_date=date(50, 5, 8),
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 4",
                                          infos="Ein Test Datum",
                                          era=self.klassik)
        return b1, b2, b3, b4, hd1, hd2, hd3, hd4

    def test_thumbnail_empty(self):
        """
        Tests for thumbnail assignment and sorting: empty thumbnails
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus':
                              (self.hellenismus, [(True, b, "100 v.Chr.", thumbnail_default)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_disabled(self):
        """
        Tests for thumbnail assignment and sorting: thumbnail, but not assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        p = Picture.objects.create(name="Test", picture=image_mock, building=b,
                                   usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus':
                              (self.hellenismus, [(True, b, "100 v.Chr.", thumbnail_default)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_enabled(self):
        """
        Tests for thumbnail assignment and sorting: thumbnail, assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        p = Picture.objects.create(name="Test", picture=image_mock,
                                   building=b, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, b, "100 v.Chr.", p)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_disabled(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, all not assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        p1 = Picture.objects.create(name="Test", picture=image_mock,
                                    building=b, usable_as_thumbnail=False)
        p2 = Picture.objects.create(name="Test", picture=image_mock2,
                                    building=b, usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (
                          self.hellenismus, [(True, b, "100 v.Chr.", thumbnail_default)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_both1(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, one assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        p1 = Picture.objects.create(name="Test", picture=image_mock,
                                    building=b, usable_as_thumbnail=True)
        p2 = Picture.objects.create(name="Test", picture=image_mock2,
                                    building=b, usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, b, "100 v.Chr.", p1)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_both2(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, one other assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        p1 = Picture.objects.create(name="Test", picture=image_mock,
                                    building=b, usable_as_thumbnail=False)
        p2 = Picture.objects.create(name="Test", picture=image_mock2,
                                    building=b, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, b, "100 v.Chr.", p2)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_enabled(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, all assigned
        :return: None / Test results
        """
        b = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")

        p1 = Picture.objects.create(name="Test", picture=image_mock,
                                    building=b, usable_as_thumbnail=True)
        p2 = Picture.objects.create(name="Test", picture=image_mock2,
                                    building=b, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, b, "100 v.Chr.", p1)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    class GetDateAsStingTests(TestCase):
        """
        Tests for class method get_date_as_string(item), witch returns the date in best manner,
        as string.
        """

        @classmethod
        def setUpTestData(cls):
            """
            Just a simple setup for some test data.
            :return: All these Buildings and HistoricDates defined beneath
            """
            cls.client = Client()
            cls.bronzezeit = Era.objects.create(name="Bronzezeit", year_from=1400,
                                                year_from_BC_or_AD="v.Chr.",
                                                year_to=1100,
                                                year_to_BC_or_AD="v.Chr.",
                                                visible_on_video_page=True,
                                                color_code="fffff1")
            cls.frühzeit = Era.objects.create(name="Frühzeit", year_from=1100,
                                              year_from_BC_or_AD="v.Chr.", year_to=700,
                                              year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                              color_code="fffff2")
            cls.archaik = Era.objects.create(name="Archaik", year_from=700,
                                             year_from_BC_or_AD="v.Chr.",
                                             year_to=500,
                                             year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                             color_code="fffff3")
            cls.klassik = Era.objects.create(name="Klassisk", year_from=500,
                                             year_from_BC_or_AD="v.Chr.", year_to=336,
                                             year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                             color_code="fffff4")
            cls.hellenismus = Era.objects.create(name="Hellenismus", year_from=336,
                                                 year_from_BC_or_AD="v.Chr.", year_to=100,
                                                 year_to_BC_or_AD="n.Chr.",
                                                 visible_on_video_page=True,
                                                 color_code="fffff5")
            cls.b1 = Building.objects.create(name="Building 1", year_from=100,
                                             year_from_BC_or_AD="v.Chr.")
            cls.b2 = Building.objects.create(name="Building 2", year_from=5,
                                             year_from_BC_or_AD="v.Chr.")
            cls.b3 = Building.objects.create(name="Building 3", year_from=10,
                                             year_from_BC_or_AD="n.Chr.")
            cls.b4 = Building.objects.create(name="Building 4", year_from=100,
                                             year_from_BC_or_AD="n.Chr.")
            cls.b1ca = Building.objects.create(name="Building 1", year_from=100,
                                             year_from_BC_or_AD="v.Chr.", year_ca=True)
            cls.b2jh = Building.objects.create(name="Building 2", year_from=5,
                                             year_from_BC_or_AD="v.Chr.",
                                             year_century=True)
            cls.b2jhca = Building.objects.create(name="Building 2", year_from=5,
                                             year_from_BC_or_AD="v.Chr.",
                                             year_century=True, year_ca=True)


            cls.hd1 = HistoricDate.objects.create(year=50, exacter_date=date(50, 3, 27),
                                                  year_BC_or_AD="v.Chr.",
                                                  title="Historic Date 1",
                                                  infos="Ein Test Datum",
                                                  era=cls.bronzezeit)
            cls.hd2 = HistoricDate.objects.create(year=0, exacter_date=date(1, 1, 1),
                                                  year_BC_or_AD="v.Chr.",
                                                  title="Historic Date 2",
                                                  infos="Ein Test Datum",
                                                  era=cls.frühzeit)
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
            cls.hd5ca = HistoricDate.objects.create(year=50, exacter_date=None,
                                                  year_BC_or_AD="v.Chr.",
                                                  title="Historic Date 1",
                                                  infos="Ein Test Datum",
                                                  era=cls.bronzezeit, year_ca=True)
            cls.hd5jh = HistoricDate.objects.create(year=50, exacter_date=None,
                                                  year_BC_or_AD="v.Chr.",
                                                  title="Historic Date 1",
                                                  infos="Ein Test Datum",
                                                  era=cls.bronzezeit, year_century=True)
            cls.hd5jhca = HistoricDate.objects.create(year=50, exacter_date=None,
                                                  year_BC_or_AD="v.Chr.",
                                                  title="Historic Date 1",
                                                  infos="Ein Test Datum",
                                                  era=cls.bronzezeit, year_ca=True,
                                                  year_century=True)


        def test_getDates(self):
            """
            Test the date result as str. Caution: Tests run with locale="en-EN",
            Date-Format is other than it might be in german environment!
            :return: None / Test results
            """
            self.assertEqual(get_date_as_str((self.b1,)), "100 v.Chr.")
            self.assertEqual(get_date_as_str((self.b2,)), "5 v.Chr.")
            self.assertEqual(get_date_as_str((self.b3,)), "10 n.Chr.")
            self.assertEqual(get_date_as_str((self.b4,)), "100 n.Chr.")
            self.assertEqual(get_date_as_str(self.hd1), "27.3.50 v.Chr.")
            self.assertEqual(get_date_as_str(self.hd2), "1.1.1 v.Chr.")
            self.assertEqual(get_date_as_str(self.hd3), "0 n.Chr.")
            self.assertEqual(get_date_as_str(self.hd4), "8.7.50 n.Chr.")
            self.assertEqual(get_date_as_str((self.b1ca,)), "ca. 100 v.Chr.")
            self.assertEqual(get_date_as_str((self.b2jh,)), "5. Jh. v.Chr.")
            self.assertEqual(get_date_as_str((self.b2jhca,)), "ca. 5. Jh. v.Chr.")
            self.assertEqual(get_date_as_str(self.hd5ca), "ca. 50 v.Chr.")
            self.assertEqual(get_date_as_str(self.hd5jh), "50. Jh. v.Chr.")
            self.assertEqual(get_date_as_str(self.hd5jhca), "ca. 50. Jh. v.Chr.")


class GetStartYearOfItemTests(TestCase):
    """
    Tests for the get_start_year_of_item(i) method.
    ;return: None/Test results
    """
    @classmethod
    def setUpTestData(cls):
        """
        Just a simple setup for some test data.
        :return: All these Buildings and HistoricDates defined beneath
        """
        cls.client = Client()
        cls.bronzezeit = Era.objects.create(name="Bronzezeit", year_from=1400,
                                            year_from_BC_or_AD="v.Chr.",
                                            year_to=1100,
                                            year_to_BC_or_AD="v.Chr.",
                                            visible_on_video_page=True,
                                            color_code="fffff1")
        cls.frühzeit = Era.objects.create(name="Frühzeit", year_from=1100,
                                          year_from_BC_or_AD="v.Chr.", year_to=700,
                                          year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                          color_code="fffff2")
        cls.archaik = Era.objects.create(name="Archaik", year_from=700,
                                         year_from_BC_or_AD="v.Chr.",
                                         year_to=500,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                         color_code="fffff3")
        cls.klassik = Era.objects.create(name="Klassisk", year_from=500,
                                         year_from_BC_or_AD="v.Chr.", year_to=336,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                         color_code="fffff4")
        cls.hellenismus = Era.objects.create(name="Hellenismus", year_from=336,
                                             year_from_BC_or_AD="v.Chr.", year_to=100,
                                             year_to_BC_or_AD="n.Chr.",
                                             visible_on_video_page=True,
                                             color_code="fffff5")
        cls.b1 = Building.objects.create(name="Building 1", year_from=100,
                                         year_from_BC_or_AD="v.Chr.")
        cls.b2 = Building.objects.create(name="Building 2", year_from=5,
                                         year_from_BC_or_AD="v.Chr.")
        cls.b3 = Building.objects.create(name="Building 3", year_from=10,
                                         year_from_BC_or_AD="n.Chr.")
        cls.b4 = Building.objects.create(name="Building 4", year_from=100,
                                         year_from_BC_or_AD="n.Chr.")
        cls.b1ca = Building.objects.create(name="Building 1", year_from=100,
                                         year_from_BC_or_AD="v.Chr.", year_ca=True)
        cls.b2jh = Building.objects.create(name="Building 2", year_from=5,
                                         year_from_BC_or_AD="v.Chr.",
                                         year_century=True)
        cls.b2jhca = Building.objects.create(name="Building 2", year_from=5,
                                         year_from_BC_or_AD="v.Chr.",
                                         year_century=True, year_ca=True)


        cls.hd1 = HistoricDate.objects.create(year=50, exacter_date=date(50, 3, 27),
                                              year_BC_or_AD="v.Chr.",
                                              title="Historic Date 1",
                                              infos="Ein Test Datum",
                                              era=cls.bronzezeit)
        cls.hd2 = HistoricDate.objects.create(year=0, exacter_date=date(1, 1, 1),
                                              year_BC_or_AD="v.Chr.",
                                              title="Historic Date 2",
                                              infos="Ein Test Datum",
                                              era=cls.frühzeit)
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
        cls.hd5ca = HistoricDate.objects.create(year=50, exacter_date=None,
                                              year_BC_or_AD="v.Chr.",
                                              title="Historic Date 1",
                                              infos="Ein Test Datum",
                                              era=cls.bronzezeit, year_ca=True)
        cls.hd5jh = HistoricDate.objects.create(year=50, exacter_date=None,
                                              year_BC_or_AD="v.Chr.",
                                              title="Historic Date 1",
                                              infos="Ein Test Datum",
                                              era=cls.bronzezeit, year_century=True)
        cls.hd5jhca = HistoricDate.objects.create(year=50, exacter_date=None,
                                              year_BC_or_AD="v.Chr.",
                                              title="Historic Date 1",
                                              infos="Ein Test Datum",
                                              era=cls.bronzezeit, year_ca=True,
                                              year_century=True)

    def test_get_start_year_of_item(self):
        """
        Tests for the get_start_year_of_item method.
        ;return: None / Test results
        """
        self.assertEqual(get_start_year_of_item((self.b1,)), -100)
        self.assertEqual(get_start_year_of_item((self.b2,)), -5)
        self.assertEqual(get_start_year_of_item((self.b3,)), 10)
        self.assertEqual(get_start_year_of_item((self.b4,)), 100)
        self.assertEqual(get_start_year_of_item(self.hd1), -50)
        self.assertEqual(get_start_year_of_item(self.hd2), -1)
        self.assertEqual(get_start_year_of_item(self.hd3), 0)
        self.assertEqual(get_start_year_of_item(self.hd4), 50)
        self.assertEqual(get_start_year_of_item((self.b1ca,)), -100)
        self.assertEqual(get_start_year_of_item((self.b2jh,)), -450)
        self.assertEqual(get_start_year_of_item((self.b2jhca,)), -450)
        self.assertEqual(get_start_year_of_item(self.hd5ca), -50)
        self.assertEqual(get_start_year_of_item(self.hd5jh), -4950)
        self.assertEqual(get_start_year_of_item(self.hd5jhca), -4950)


class TestsCasesSortedBuildings(TestCase):
    """
    Test Cases for the function sorted_eras_with_buildings
    """

    def setUp(self):
        """
        Setting up a client for the responses
        """
        self.client = Client()

    def test1_sorted_eras_with_buildings(self):
        """
        Testing the function sorted_eras_with_buildings
        Case: No eras and buildings
        """
        response = self.client.get('/timeline/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Eras_Buildings'], {})

    def test2_sorted_eras_with_buildings(self):
        """
        Testing the function sorted_eras_with_buildings
        Case: Some eras with no buildings
        """

        klassik = Era.objects.create(name="Klassik", year_from=500,
                                     year_from_BC_or_AD="v.Chr.", year_to=337,
                                     year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                     color_code="fffff4")
        hellenismus = Era.objects.create(name="Hellenismus", year_from=337,
                                         year_from_BC_or_AD="v.Chr.", year_to=30,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                         color_code="fffff5")
        kaiserzeit = Era.objects.create(name='Kaiserzeit', year_from=30,
                                        year_from_BC_or_AD='n.Chr.', year_to=284,
                                        year_to_BC_or_AD='n.Chr.',
                                        visible_on_video_page=True)

        response = self.client.get('/timeline/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Eras_Buildings'],
                         {'Klassik': (klassik, []),
                          'Hellenismus': (hellenismus, []),
                          'Kaiserzeit': (kaiserzeit, [])})

    def test3_sorted_eras_with_buildings(self):
        """
        Testing with all eras and many buildings and historic dates
        """
        bronzezeit = Era.objects.create(name="Bronzezeit", year_from=1400,
                                        year_from_BC_or_AD="v.Chr.",
                                        year_to=1100,
                                        year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                        color_code="fffff1")
        frühzeit = Era.objects.create(name="Frühzeit", year_from=1100,
                                      year_from_BC_or_AD="v.Chr.", year_to=700,
                                      year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                      color_code="fffff2")
        archaik = Era.objects.create(name="Archaik", year_from=700, year_from_BC_or_AD="v.Chr.",
                                     year_to=500,
                                     year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                     color_code="fffff3")
        klassik = Era.objects.create(name="Klassik", year_from=500,
                                     year_from_BC_or_AD="v.Chr.", year_to=337,
                                     year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                     color_code="fffff4")
        hellenismus = Era.objects.create(name="Hellenismus", year_from=337,
                                         year_from_BC_or_AD="v.Chr.", year_to=30,
                                         year_to_BC_or_AD="v.Chr.", visible_on_video_page=True,
                                         color_code="fffff5")
        kaiserzeit = Era.objects.create(name="Kaiserzeit", year_from=30,
                                        year_from_BC_or_AD="v.Chr.", year_to=284,
                                        year_to_BC_or_AD="n.Chr.",
                                        visible_on_video_page=True)
        spätantike = Era.objects.create(name='Spätantike', year_from=284,
                                        year_from_BC_or_AD="n.Chr.", year_to=565,
                                        year_to_BC_or_AD="n.Chr.", visible_on_video_page=True)
        sonstiges = Era.objects.create(name='Sonstiges', year_from=565,
                                       year_from_BC_or_AD='n.Chr.',
                                       year_to=10000, year_to_BC_or_AD='n.Chr.')
        building1 = Building.objects.create(name='Reichstag', city='Berlin', year_from=1000,
                                            year_from_BC_or_AD='v.Chr.',
                                            country='Deutschland', region='Berlin',
                                            era=frühzeit, architect='Jonathan Otto',
                                            context='Regierungsgebäude',
                                            builder='Ganesha Welsch',
                                            construction_type='Erhaben', design='erniedrigend',
                                            function='Regierung', column_order='ionisch',
                                            material='Stein', construction='Massivbau')
        building2 = Building.objects.create(name='Eiffelturm', city='Paris', year_from=200,
                                            year_from_BC_or_AD='n.Chr.',
                                            country='Frankreich', region=None,
                                            era=kaiserzeit, architect='Jonas Günster',
                                            context='Weltausstellung',
                                            builder='Michael Wendler',
                                            construction_type='groß', design='erstaunlich',
                                            function='Denkmal', column_order='vier',
                                            material='Stahl', construction=None)
        building3 = Building.objects.create(name='Hagia Sophia', city='Istanbul', year_from=499,
                                            year_from_BC_or_AD='v.Chr.',
                                            country='Turkey', region='Berlin',
                                            era=archaik, architect='Manuel Singer',
                                            context='Moschee',
                                            builder='Philipp Krause',
                                            construction_type='Moschee', design='Großartig',
                                            function='Heiligtum', column_order='dorisch',
                                            material='Marmor', construction='Massivbau')
        building4 = Building.objects.create(name='Brandenburger Tor', city='Berlin',
                                            year_from=1199,
                                            year_from_BC_or_AD='v.Chr.',
                                            country='Deutschland', region='Berlin',
                                            era=frühzeit, architect='Philipp Krause',
                                            context='Symbol',
                                            builder='Jonathan Otto',
                                            construction_type='Erhaben', design='erniedrigend',
                                            function='Regierung', column_order='dorisch',
                                            material='Stein', construction='Massivbau')
        building5 = Building.objects.create(name='Bundestag', city='Berlin', year_from=1,
                                            year_from_BC_or_AD='v.Chr.', year_century=True,
                                            country='Deutschland', region='Berlin',
                                            era=hellenismus, architect='Simon Gröger',
                                            context='Regierungsgebäude',
                                            builder='Ganesha Welsch',
                                            construction_type='Erhaben', design='erniedrigend',
                                            function='Regierung', column_order='ionisch',
                                            material='Stein', construction='Massivbau')
        building6 = Building.objects.create(name='Alexander Platz', city='Berlin',
                                            year_from=753,
                                            year_from_BC_or_AD='n.Chr.',
                                            country='Deutschland', region='Berlin',
                                            era=frühzeit, architect='Jonathan Otto',
                                            context='Regierungsgebäude',
                                            builder='Ganesha Welsch',
                                            construction_type='Platzartig', design='neuartig',
                                            function='Regierung', column_order='dorisch',
                                            material='Ziegel', construction='Massivbau')
        building7 = Building.objects.create(name='Pompeji', city='Pompeji', year_from=5,
                                            year_from_BC_or_AD='n.Chr.', year_century=True,
                                            country='Italien', region='Kampanien',
                                            era=kaiserzeit, architect=None,
                                            context='Historische Stadt',
                                            builder=None,
                                            construction_type='Langlebig', design='aschig',
                                            function='Stadt', column_order=None,
                                            material='Stein', construction='Städtisch')
        building8 = Building.objects.create(name='Rosinen', city='Darmstadt', year_from=345,
                                            year_from_BC_or_AD='n.Chr.',
                                            country='Deutschland', region='Hessen',
                                            era=klassik, architect='Laura Buhleier',
                                            context='Essen',
                                            builder='Quang Nguyen',
                                            construction_type='Gesund', design='schrumpelig',
                                            function='Ernährung', column_order=None,
                                            material='Trauben', construction='trocknen')
        building9 = Building.objects.create(name='TU', city='Darmstadt', year_from=777,
                                            year_from_BC_or_AD='v.Chr.',
                                            country='Deutschland', region='Hessen',
                                            era=archaik, architect=None,
                                            context='Universität',
                                            builder='Ganesha Welsch',
                                            construction_type='Unterwürfig', design=None,
                                            function='Forschung', column_order='toskanisch',
                                            material='Stein', construction='Massivbau')
        building10 = Building.objects.create(name='Klingon', city=None, year_from=0,
                                             country=None, region=None,
                                             era=spätantike, architect='Spock',
                                             context='Planet der Klingonen',
                                             builder='Michael Burnham',
                                             construction_type=None, design='tödlich',
                                             function='Destroy', column_order='klingonisch',
                                             material='Planet', construction='Massiv')
        building11 = Building.objects.create(name='Kölner Dom', city='Köln',
                                             country='China', region='Texas',
                                             era=sonstiges, architect='Winnie Puuh',
                                             context='Parody',
                                             builder='Tebarts van Elst',
                                             construction_type='Money', design='Prunk',
                                             function='Fegefeuer', column_order='komposite',
                                             material='Münzen', construction='Fort')

        hd1 = HistoricDate.objects.create(year=50, exacter_date=date(50, 3, 27),
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 1",
                                          infos="Ein Test Datum",
                                          era=bronzezeit)
        hd2 = HistoricDate.objects.create(year=0, exacter_date=date(751, 1, 1),
                                          year_BC_or_AD="v.Chr.",
                                          title="Historic Date 2",
                                          infos="Ein Test Datum",
                                          era=frühzeit)
        hd3 = HistoricDate.objects.create(year=3, exacter_date=None, year_century=True,
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 3",
                                          infos="Ein Test Datum",
                                          era=archaik)
        hd4 = HistoricDate.objects.create(year=50, exacter_date=date(50, 7, 8),
                                          year_BC_or_AD="n.Chr.",
                                          title="Historic Date 4",
                                          infos="Ein Test Datum",
                                          era=klassik)

        self.maxDiff = None
        response = self.client.get('/timeline/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['Eras_Buildings']['Bronzezeit'],
                         (bronzezeit, [(True, building4, '1199 v.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Frühzeit'],
                         (frühzeit, [(True, building1, '1000 v.Chr.', None),
                                     (True, building9, '777 v.Chr.', None),
                                     (False, hd2, '1.1.751 v.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Archaik'], (archaik, []))
        self.assertEqual(response.context['Eras_Buildings']['Klassik'],
                         (klassik, [(True, building3, '499 v.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Hellenismus'],
                         (hellenismus, [(True, building5, '1. Jh. v.Chr.', None),
                                        (False, hd1, '27.3.50 v.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Kaiserzeit'],
                         (kaiserzeit, [(True, building10, '0 n.Chr.', None),
                                       (False, hd4, '8.7.50 n.Chr.', None),
                                       (True, building2, '200 n.Chr.', None),
                                       (False, hd3, '3. Jh. n.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Spätantike'],
                         (spätantike, [(True, building8, '345 n.Chr.', None),
                                       (True, building7, '5. Jh. n.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Sonstiges'],
                         (sonstiges, [(True, building6, '753 n.Chr.', None),
                                      (True, building11, '9999 n.Chr.', None)]))

        self.assertEqual(response.context['Eras_Buildings'],
                         {'Bronzezeit': (bronzezeit, [(True, building4, '1199 v.Chr.', None)]),
                          'Frühzeit': (frühzeit, [(True, building1, '1000 v.Chr.', None),
                                                  (True, building9, '777 v.Chr.', None),
                                                  (False, hd2, '1.1.751 v.Chr.', None)]),
                          'Archaik': (archaik, []),
                          'Klassik': (klassik, [(True, building3, '499 v.Chr.', None)]),
                          'Hellenismus': (
                              hellenismus, [(True, building5, '1. Jh. v.Chr.', None),
                                            (False, hd1, '27.3.50 v.Chr.', None),
                                            ]),
                          'Kaiserzeit': (kaiserzeit, [(True, building10, '0 n.Chr.', None),
                                                      (False, hd4, '8.7.50 n.Chr.', None),
                                                      (True, building2, '200 n.Chr.', None),
                                                      (False, hd3, '3. Jh. n.Chr.', None)]),
                          'Spätantike': (spätantike, [(True, building8, '345 n.Chr.', None),
                                                      (
                                                          True, building7, '5. Jh. n.Chr.',
                                                          None)]),
                          'Sonstiges': (sonstiges, [(True, building6, '753 n.Chr.', None),
                                                    (True, building11, '9999 n.Chr.', None)])})
