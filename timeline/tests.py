"""
Tests for functions in the App: timeline
"""
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from timeline.models import HistoricDate
from timeline.views import sorted_eras_with_buildings
from details_page.models import Era, Building, Picture

# Define some temp images for testing
Thumbnail_Default = None
Test_Image = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
              b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
              b'\x02\x4c\x01\x00\x3b')
image_mock = SimpleUploadedFile('small.img', Test_Image, content_type='image/gif')
image_mock2 = SimpleUploadedFile('small.img', Test_Image, content_type='image/gif')


class HistoricDatesModelTests(TestCase):
    # pylint: disable = no-member
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
        """
        Testing if the response returns the ok status code
        """
        response = self.client.get('/timeline/')
        self.assertEqual(response.status_code, 200)

    def test_entries_correct(self):
        """
        Test the entries if correct data was given
        :return: None / Test results
        """
        hd1 = HistoricDate.objects.create(year=17, exacter_date=None, year_BC_or_AD="n.Chr.",
                                          title="Test Datum", infos="Ein Test Datum",
                                          era=self.an_era)
        self.assertEqual(HistoricDate.objects.get(title="Test Datum"), hd1)
        self.assertEqual(HistoricDate.objects.get(pk=1).year, hd1.year)
        self.assertEqual(HistoricDate.objects.get(pk=1).exacter_date, hd1.exacter_date)
        self.assertEqual(HistoricDate.objects.get(pk=1).year_BC_or_AD, hd1.year_BC_or_AD)
        self.assertEqual(HistoricDate.objects.get(pk=1).title, hd1.title)
        self.assertEqual(HistoricDate.objects.get(pk=1).infos, hd1.infos)
        self.assertEqual(HistoricDate.objects.get(pk=1).era, hd1.era)

    def test__str__(self):
        """
        Tests for the __str__ method of the model
        :return: None / Test results
        """
        # for just a year number
        hd1 = HistoricDate.objects.create(year=23, exacter_date=None,
                                          year_BC_or_AD="n.Chr.",
                                          title="Test",
                                          infos="Ein Test Datum",
                                          era=self.an_era)
        self.assertEqual(str(HistoricDate.objects.get(title="Test")), str(hd1.title)
                         + " (" + str(hd1.year) + " "
                         + str(hd1.year_BC_or_AD) + ")")
        # with exacter date
        hd1.exacter_date = date(23, 3, 1)
        hd1.save()
        self.assertEqual(str(HistoricDate.objects.get(title="Test")), str(hd1.title)
                         + " (" + '1.3.23 n.Chr.' + ")")

    @staticmethod
    def setup_historic_dates():
        """
        Setting up some historic dates
        """
        hd1 = HistoricDate.objects.create()
        hd2 = HistoricDate.objects.create(year=0, exacter_date=date(2, 1, 1),
                                          year_BC_or_AD="n.Chr.")
        hd3 = HistoricDate.objects.create(year=100, year_BC_or_AD="v.Chr.")
        hd4 = HistoricDate.objects.create(year=100, year_BC_or_AD="n.Chr.", year_ca=True)
        hd5 = HistoricDate.objects.create(year=100, year_BC_or_AD="v.Chr.",
                                          exacter_date=date(1, 2, 3))
        hd6 = HistoricDate.objects.create(year=1, year_BC_or_AD='v.Chr.', year_century=True)
        hd7 = HistoricDate.objects.create(year=1, year_BC_or_AD='n.Chr.', year_century=True,
                                          year_ca=True)

        return hd1, hd2, hd3, hd4, hd5, hd6, hd7

    def test_get_year_as_signed_int(self):
        """
        Testing the function get_year_as_signed_int in the historic date
        """
        hd1, hd2, hd3, hd4, hd5, hd6, hd7 = self.setup_historic_dates()

        # Getting the default year
        self.assertEqual(hd1.get_year_as_signed_int(), [9999, 9999])

        # Exact date
        self.assertEqual(hd2.get_year_as_signed_int(), [2, 9999])
        hd2.year_BC_or_AD = 'v.Chr.'
        self.assertEqual(hd2.get_year_as_signed_int(), [-2, 9999])

        # Year
        self.assertEqual(hd3.get_year_as_signed_int(), [-100, 9999])
        self.assertEqual(hd4.get_year_as_signed_int(), [100, 9999])

        # Both exists
        self.assertEqual(hd5.get_year_as_signed_int(), [-1, 9999])
        hd5.year_BC_or_AD = 'n.Chr.'
        self.assertEqual(hd5.get_year_as_signed_int(), [1, 9999])

        # Year century
        self.assertEqual(hd6.get_year_as_signed_int(), [-50, 9999])
        self.assertEqual(hd7.get_year_as_signed_int(), [50, 9999])

    def test_get_year_as_str(self):
        """
        Testing the function get_year_as_string
        """
        hd1, hd2, hd3, hd4, hd5, hd6, hd7 = self.setup_historic_dates()
        # No year and no exact_date
        self.assertEqual(hd1.get_year_as_str(), '')

        # Only Exact date
        self.assertEqual(hd2.get_year_as_str(), '1.1.2 n.Chr.')

        # Only Year
        self.assertEqual(hd3.get_year_as_str(), '100 v.Chr.')
        # with ca.
        self.assertEqual(hd4.get_year_as_str(), 'ca. 100 n.Chr.')

        # Both exists
        self.assertEqual(hd5.get_year_as_str(), '3.2.1 v.Chr.')

        # Year century
        self.assertEqual(hd6.get_year_as_str(), '1. Jh. v.Chr.')
        # with ca.
        self.assertEqual(hd7.get_year_as_str(), 'ca. 1. Jh. n.Chr.')


class TimelineViewsTest(TestCase):
    # pylint: disable = no-member
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
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        bu2 = Building.objects.create(name="Building 2", year_from=5, year_from_BC_or_AD="v.Chr.")
        bu3 = Building.objects.create(name="Building 3", year_from=10, year_from_BC_or_AD="n.Chr.")
        bu4 = Building.objects.create(name="Building 4", year_from=100, year_from_BC_or_AD="n.Chr.")

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
        return bu1, bu2, bu3, bu4, hd1, hd2, hd3, hd4

    def setup_some2(self):
        """
        Simple Setup for some test data
        :return: None
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        bu2 = Building.objects.create(name="Building 2", year_from=5, year_from_BC_or_AD="v.Chr.")
        bu3 = Building.objects.create(name="Building 3", year_from=10, year_from_BC_or_AD="n.Chr.")
        bu4 = Building.objects.create(name="Building 4", year_from=100, year_from_BC_or_AD="n.Chr.")
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
        return bu1, bu2, bu3, bu4, hd1, hd2, hd3, hd4

    def test_thumbnail_empty(self):
        """
        Tests for thumbnail assignment and sorting: empty thumbnails
        :return: None / Test results
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus':
                              (self.hellenismus, [(True, bu1, "100 v.Chr.", Thumbnail_Default)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_disabled(self):
        """
        Tests for thumbnail assignment and sorting: thumbnail, but not assigned
        :return: None / Test results
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        Picture.objects.create(name="Test", picture=image_mock, building=bu1,
                               usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus':
                              (self.hellenismus, [(True, bu1, "100 v.Chr.", Thumbnail_Default)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_enabled(self):
        """
        Tests for thumbnail assignment and sorting: thumbnail, assigned
        :return: None / Test results
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        pic = Picture.objects.create(name="Test", picture=image_mock,
                                     building=bu1, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, bu1, "100 v.Chr.", pic)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_disabled(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, all not assigned
        :return: None / Test results
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        Picture.objects.create(name="Test", picture=image_mock,
                               building=bu1, usable_as_thumbnail=False)
        Picture.objects.create(name="Test", picture=image_mock2,
                               building=bu1, usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (
                              self.hellenismus, [(True, bu1, "100 v.Chr.", Thumbnail_Default)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_both1(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, one assigned
        :return: None / Test results
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        pic1 = Picture.objects.create(name="Test", picture=image_mock,
                                      building=bu1, usable_as_thumbnail=True)
        Picture.objects.create(name="Test", picture=image_mock2,
                               building=bu1, usable_as_thumbnail=False)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, bu1, "100 v.Chr.", pic1)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_both2(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, one other assigned
        :return: None / Test results
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")
        Picture.objects.create(name="Test", picture=image_mock,
                               building=bu1, usable_as_thumbnail=False)
        pic2 = Picture.objects.create(name="Test", picture=image_mock2,
                                      building=bu1, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, bu1, "100 v.Chr.", pic2)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                         )

    def test_thumbnail_more_enabled(self):
        """
        Tests for thumbnail assignment and sorting: more thumbnails, all assigned
        :return: None / Test results
        """
        bu1 = Building.objects.create(name="Building 1", year_from=100, year_from_BC_or_AD="v.Chr.")

        pic1 = Picture.objects.create(name="Test", picture=image_mock,
                                      building=bu1, usable_as_thumbnail=True)
        Picture.objects.create(name="Test", picture=image_mock2,
                               building=bu1, usable_as_thumbnail=True)
        response = self.client.get("/timeline/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["Eras_Buildings"],
                         {'Bronzezeit': (self.bronzezeit, []),
                          'Frühzeit': (self.frühzeit, []),
                          'Archaik': (self.archaik, []),
                          'Klassik': (self.klassik, []),
                          'Hellenismus': (self.hellenismus, [(True, bu1, "100 v.Chr.", pic1)]),
                          'Kaiserzeit': (self.kaiserzeit, []),
                          'Spätantike': (self.spätantike, [])}
                        )
       

def setup():
    # pylint: disable = no-member
    """
    Setting up all eras, some buildings and some historic dates
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
    return bronzezeit, frühzeit, archaik, klassik, hellenismus, kaiserzeit, spätantike, sonstiges, \
           building1, building2, building3, building4, building5, building6, building7, building8, \
           building9, building10, building11, hd1, hd2, hd3, hd4


class TestsCasesSortedBuildings(TestCase):
    # pylint: disable = no-member
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
        bronzezeit, frühzeit, archaik, klassik, hellenismus, kaiserzeit, spätantike, sonstiges, \
        building1, building2, building3, building4, building5, building6, building7, building8, \
        building9, building10, building11, hd1, hd2, hd3, hd4 = setup()

        building_list = [building1, building2, building3, building4, building5, building6,
                         building7, building8, building9, building10, building11]
        test_list = building_list + [hd1, hd2,
                                     hd3, hd4]

        self.maxDiff = None
        response = self.client.get('/timeline/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(sorted_eras_with_buildings(test_list)['Bronzezeit'],
                         (bronzezeit, [(True, building4, '1199 v.Chr.', None)]))
        self.assertEqual(sorted_eras_with_buildings(test_list)['Frühzeit'],
                         (frühzeit, [(True, building1, '1000 v.Chr.', None),
                                     (True, building9, '777 v.Chr.', None),
                                     (False, hd2, '1.1.751 v.Chr.', None)]))
        self.assertEqual(sorted_eras_with_buildings(test_list)['Archaik'], (archaik, []))
        self.assertEqual(sorted_eras_with_buildings(test_list)['Klassik'],
                         (klassik, [(True, building3, '499 v.Chr.', None)]))
        self.assertEqual(sorted_eras_with_buildings(test_list)['Hellenismus'],
                         (hellenismus, [(True, building5, '1. Jh. v.Chr.', None),
                                        (False, hd1, '27.3.50 v.Chr.', None)]))
        self.assertEqual(sorted_eras_with_buildings(test_list)['Kaiserzeit'],
                         (kaiserzeit, [(True, building10, '0 v.Chr.', None),
                                       (False, hd4, '8.7.50 n.Chr.', None),
                                       (True, building2, '200 n.Chr.', None),
                                       (False, hd3, '3. Jh. n.Chr.', None)]))
        self.assertEqual(sorted_eras_with_buildings(test_list)['Spätantike'],
                         (spätantike, [(True, building8, '345 n.Chr.', None),
                                       (True, building7, '5. Jh. n.Chr.', None)]))
        self.assertEqual(sorted_eras_with_buildings(test_list)['Sonstiges'],
                         (sonstiges, [(True, building6, '753 n.Chr.', None),
                                      (True, building11, '', None)]))

        self.assertEqual(sorted_eras_with_buildings(test_list),
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
                          'Kaiserzeit': (kaiserzeit, [(True, building10, '0 v.Chr.', None),
                                                      (False, hd4, '8.7.50 n.Chr.', None),
                                                      (True, building2, '200 n.Chr.', None),
                                                      (False, hd3, '3. Jh. n.Chr.', None)]),
                          'Spätantike': (spätantike, [(True, building8, '345 n.Chr.', None),
                                                      (
                                                          True, building7, '5. Jh. n.Chr.',
                                                          None)]),
                          'Sonstiges': (sonstiges, [(True, building6, '753 n.Chr.', None),
                                                    (True, building11, '', None)])})


class TestTimeline(TestCase):
    # pylint: disable = no-member
    """
    Testing the main function timeline in timeline.views
    """

    def test(self):
        """
        We need only one test, because we testet the other functions enough
        """
        bronzezeit, frühzeit, archaik, klassik, hellenismus, kaiserzeit, spätantike, sonstiges, \
        building1, building2, building3, building4, building5, building6, building7, building8, \
        building9, building10, building11, hd1, hd2, hd3, hd4 = setup()

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
                         (kaiserzeit, [(True, building10, '0 v.Chr.', None),
                                       (False, hd4, '8.7.50 n.Chr.', None),
                                       (True, building2, '200 n.Chr.', None),
                                       (False, hd3, '3. Jh. n.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Spätantike'],
                         (spätantike, [(True, building8, '345 n.Chr.', None),
                                       (True, building7, '5. Jh. n.Chr.', None)]))
        self.assertEqual(response.context['Eras_Buildings']['Sonstiges'],
                         (sonstiges, [(True, building6, '753 n.Chr.', None),
                                      (True, building11, '', None)]))

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
                          'Kaiserzeit': (kaiserzeit, [(True, building10, '0 v.Chr.', None),
                                                      (False, hd4, '8.7.50 n.Chr.', None),
                                                      (True, building2, '200 n.Chr.', None),
                                                      (False, hd3, '3. Jh. n.Chr.', None)]),
                          'Spätantike': (spätantike, [(True, building8, '345 n.Chr.', None),
                                                      (
                                                          True, building7, '5. Jh. n.Chr.',
                                                          None)]),
                          'Sonstiges': (sonstiges, [(True, building6, '753 n.Chr.', None),
                                                    (True, building11, '', None)])})

        # impressum = Impressum(course_link='https://moodle.tu-darmstadt.de/my/')
        # self.assertEqual(response.context['Kurs_Link'], 'https://moodle.tu-darmstadt.de/my/')
