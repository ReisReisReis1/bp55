"""
Tests for the functions in the App: search
"""
# pylint: disable=all
from django.test import TestCase, Client
# pylint: disable = import-error
from details_page.models import Building, Era

TEST_PICTURE_PATH = '/static/default-thumbnail.png'


class SearchTestCases(TestCase):
    """
    Cases to test the search function
    """

    def setUp(self):
        """
        Setting up some random test data
        """
        self.frühzeit = Era.objects.create(name='Frühzeit')
        self.archaik = Era.objects.create(name='Archaik')
        self.hellenismus = Era.objects.create(name='Helenismus')
        self.römisch = Era.objects.create(name='Römische Kaiserzeit')
        self.klassik = Era.objects.create(name='Klassik')
        self.spätantike = Era.objects.create(name='Spätantike')
        self.sonstiges = Era.objects.create(name='Sonstiges')

        self.client = Client()

        self.building1 = Building.objects.create(name='Reichstag', city='Berlin',
                                                 country='Deutschland', region='Berlin',
                                                 era=self.frühzeit, architect='Jonathan Otto',
                                                 context='Regierungsgebäude',
                                                 builder='Ganesha Welsch',
                                                 construction_type='Erhaben', design='erniedrigend',
                                                 function='Regierung', column_order='ionisch',
                                                 material='Stein', construction='Massivbau')
        self.building2 = Building.objects.create(name='Eiffelturm', city='Paris',
                                                 country='Frankreich', region='',
                                                 era=self.römisch, architect='Jonas Günster',
                                                 context='Weltausstellung',
                                                 builder='Michael Wendler',
                                                 construction_type='groß', design='erstaunlich',
                                                 function='Denkmal', column_order='vier',
                                                 material='Stahl', construction='')
        self.building3 = Building.objects.create(name='Hagia Sophia', city='Istanbul',
                                                 country='Turkey', region='Berlin',
                                                 era=self.archaik, architect='Manuel Singer',
                                                 context='Moschee',
                                                 builder='Philipp Krause',
                                                 construction_type='Moschee', design='Großartig',
                                                 function='Heiligtum', column_order='dorisch',
                                                 material='Marmor', construction='Massivbau')
        self.building4 = Building.objects.create(name='Brandenburger Tor', city='Berlin',
                                                 country='Deutschland', region='Berlin',
                                                 era=self.frühzeit, architect='Philipp Krause',
                                                 context='Symbol',
                                                 builder='Jonathan Otto',
                                                 construction_type='Erhaben', design='Erniedrigend',
                                                 function='Regierung', column_order='dorisch',
                                                 material='Stein', construction='Massivbau')
        self.building5 = Building.objects.create(name='Bundestag', city='Berlin',
                                                 country='Deutschland', region='Berlin',
                                                 era=self.hellenismus, architect='Simon Gröger',
                                                 context='Regierungsgebäude',
                                                 builder='Ganesha Welsch',
                                                 construction_type='Erhaben', design='erniedrigend',
                                                 function='Regierung', column_order='ionisch',
                                                 material='Ziegel', construction='Massivbau')
        self.building6 = Building.objects.create(name='Alexander Platz', city='Berlin',
                                                 country='Deutschland', region='Berlin',
                                                 era=self.frühzeit, architect='Jonathan Otto',
                                                 context='Regierungsgebäude',
                                                 builder='Ganesha Welsch',
                                                 construction_type='Platzartig', design='neuartig',
                                                 function='Regierung', column_order='dorisch',
                                                 material='Stein', construction='Massivbau')
        self.building7 = Building.objects.create(name='Pompeji', city='Pompeji',
                                                 country='Italien', region='Kampanien',
                                                 era=self.römisch, architect='',
                                                 context='Historische Stadt',
                                                 builder='',
                                                 construction_type='Langlebig', design='aschig',
                                                 function='Stadt', column_order='',
                                                 material='Stein', construction='Städtisch')
        self.building8 = Building.objects.create(name='Rosinen', city='Darmstadt',
                                                 country='Deutschland', region='Hessen',
                                                 era=self.klassik, architect='Laura Buhleier',
                                                 context='Essen',
                                                 builder='Quang Ngyuen',
                                                 construction_type='Gesund', design='schrumpelig',
                                                 function='Ernährung', column_order='',
                                                 material='Trauben', construction='trocknen')
        self.building9 = Building.objects.create(name='TU', city='Darmstadt',
                                                 country='Deutschland', region='Hessen',
                                                 era=self.archaik, architect='',
                                                 context='Universität',
                                                 builder='Ganesha Welsch',
                                                 construction_type='Unterwürfig', design='',
                                                 function='Forschung', column_order='toskanisch',
                                                 material='Stein', construction='Massivbau')
        self.building10 = Building.objects.create(name='Klingon', city='',
                                                  country='', region='',
                                                  era=self.spätantike, architect='Spock ',
                                                  context='Planet dert Klingonen',
                                                  builder='Michael Burnham',
                                                  construction_type='', design='tödlich',
                                                  function='Desytroy', column_order='klingonisch',
                                                  material='Planet', construction='Massiv')
        self.building11 = Building.objects.create(name='Kölner Dom', city='Köln',
                                                  country='China', region='Texas',
                                                  era=self.sonstiges, architect='Winnie Puuh',
                                                  context='Parody',
                                                  builder='Tebarts van Elst',
                                                  construction_type='Money', design='Prunk',
                                                  function='Fegefeuer', column_order='komposite',
                                                  material='Münzen', construction='Fort')

    def test1(self):
        """
        Testing the search function
        No return and status code
        """
        response = self.client.get('/search/?search_request=jsvkjdfvjkdfnhfd')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['Result']), [])

    def test2(self):
        """
        Testing the search function
        One Return
        """
        response1 = self.client.get('/search/?search_request=' + self.building11.name)
        response2 = self.client.get('/search/?search_request=' + self.building11.city)
        response3 = self.client.get('/search/?search_request=' + self.building11.region)
        response4 = self.client.get('/search/?search_request=' + self.building11.country)
        response5 = self.client.get('/search/?search_request=' + self.building11.era.name)
        response6 = self.client.get('/search/?search_request=' + self.building11.architect)
        response7 = self.client.get('/search/?search_request=' + self.building11.context)
        response8 = self.client.get('/search/?search_request=' + self.building11.builder)
        response9 = self.client.get('/search/?search_request=' + self.building11.construction_type)
        response10 = self.client.get('/search/?search_request=' + self.building11.design)
        response11 = self.client.get('/search/?search_request=' + self.building11.function)
        response12 = self.client.get('/search/?search_request=' + self.building11.column_order)
        response13 = self.client.get('/search/?search_request=' + self.building11.material)

        self.assertListEqual(list(response1.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response2.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response3.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response4.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response5.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response6.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response7.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response8.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response9.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response10.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response11.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response12.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response13.context['Result']),
                             [(self.building11, test_picture_path)])

    def test3(self):
        """
        Testing the search function
        Multiple elements return
        """

        response1 = self.client.get('/search/?search_request=h')
        response2 = self.client.get('/search/?search_request=LAND')
        response3 = self.client.get('/search/?search_request=haus')
        response4 = self.client.get('/search/?search_request=Frühzeit')
        response5 = self.client.get('/search/?search_request=DEutScHlaNd')
        response6 = self.client.get('/search/?search_request=Dutschland')
        response7 = self.client.get('/search/?search_request=Kölner DOM')
        response8 = self.client.get('/search/?search_request=')
        all_buildings_ordered = [(self.building6, test_picture_path),
                                 (self.building4, test_picture_path),
                                 (self.building5, test_picture_path),
                                 (self.building2, test_picture_path),
                                 (self.building3, test_picture_path),
                                 (self.building10, test_picture_path),
                                 (self.building11, test_picture_path),
                                 (self.building7, test_picture_path),
                                 (self.building1, test_picture_path),
                                 (self.building8, test_picture_path),
                                 (self.building9, test_picture_path)]
        self.assertListEqual(list(response1.context['Result']), all_buildings_ordered)
        self.assertListEqual(list(response2.context['Result']),
                             [(self.building6, test_picture_path),
                              (self.building4, test_picture_path),
                              (self.building5, test_picture_path),
                              (self.building1, test_picture_path),
                              (self.building8, test_picture_path),
                              (self.building9, test_picture_path)
                              ])
        self.assertListEqual(list(response3.context['Result']), [])
        self.assertListEqual(list(response4.context['Result']),
                             [(self.building6, test_picture_path),
                              (self.building4, test_picture_path),
                              (self.building1, test_picture_path)])
        self.assertListEqual(list(response5.context['Result']),
                             [(self.building6, test_picture_path),
                              (self.building4, test_picture_path),
                              (self.building5, test_picture_path),
                              (self.building1, test_picture_path),
                              (self.building8, test_picture_path),
                              (self.building9, test_picture_path)])
        self.assertListEqual(list(response6.context['Result']), [])
        self.assertListEqual(list(response7.context['Result']),
                             [(self.building11, test_picture_path)])
        self.assertListEqual(list(response8.context['Result']), all_buildings_ordered)
