"""
Tests for functions in the App: home
"""
# pylint: disable=all


from django.test import Client, TestCase
# pylint: disable=import-error
from model_bakery import baker
from details_page.models import Building, Era


def setup():
    """
    Setting up some test data
    """
    frühzeit = Era.objects.create(name='Frühzeit')
    archaik = Era.objects.create(name='Archaik')
    hellenismus = Era.objects.create(name='Hellenismus')
    römisch = Era.objects.create(name='Römische Kaiserzeit')
    klassik = Era.objects.create(name='Klassik')
    spätantike = Era.objects.create(name='Spätantike')
    sonstiges = Era.objects.create(name='Sonstiges')

    building1 = Building.objects.create(name='Reichstag', city='Berlin',
                                        country='Deutschland', region='Berlin',
                                        era=frühzeit, architect='Jonathan Otto',
                                        context='Regierungsgebäude',
                                        builder='Ganesha Welsch',
                                        construction_type='Erhaben', design='erniedrigend',
                                        function='Regierung', column_order='ionisch',
                                        material='Stein', construction='Massivbau')
    building2 = Building.objects.create(name='Eiffelturm', city='Paris',
                                        country='Frankreich', region=None,
                                        era=römisch, architect='Jonas Günster',
                                        context='Weltausstellung',
                                        builder='Michael Wendler',
                                        construction_type='groß', design='erstaunlich',
                                        function='Denkmal', column_order='vier',
                                        material='Stahl', construction=None)
    building3 = Building.objects.create(name='Hagia Sophia', city='Istanbul',
                                        country='Turkey', region='Berlin',
                                        era=archaik, architect='Manuel Singer',
                                        context='Moschee',
                                        builder='Philipp Krause',
                                        construction_type='Moschee', design='Großartig',
                                        function='Heiligtum', column_order='dorisch',
                                        material='Marmor', construction='Massivbau')
    building4 = Building.objects.create(name='Brandenburger Tor', city='Berlin',
                                        country='Deutschland', region='Berlin',
                                        era=frühzeit, architect='Philipp Krause',
                                        context='Symbol',
                                        builder='Jonathan Otto',
                                        construction_type='Erhaben', design='erniedrigend',
                                        function='Regierung', column_order='dorisch',
                                        material='Stein', construction='Massivbau')
    building5 = Building.objects.create(name='Bundestag', city='Berlin',
                                        country='Deutschland', region='Berlin',
                                        era=hellenismus, architect='Simon Gröger',
                                        context='Regierungsgebäude',
                                        builder='Ganesha Welsch',
                                        construction_type='Erhaben', design='erniedrigend',
                                        function='Regierung', column_order='ionisch',
                                        material='Stein', construction='Massivbau')
    building6 = Building.objects.create(name='Alexander Platz', city='Berlin',
                                        country='Deutschland', region='Berlin',
                                        era=frühzeit, architect='Jonathan Otto',
                                        context='Regierungsgebäude',
                                        builder='Ganesha Welsch',
                                        construction_type='Platzartig', design='neuartig',
                                        function='Regierung', column_order='dorisch',
                                        material='Ziegel', construction='Massivbau')
    building7 = Building.objects.create(name='Pompeji', city='Pompeji',
                                        country='Italien', region='Kampanien',
                                        era=römisch, architect=None,
                                        context='Historische Stadt',
                                        builder=None,
                                        construction_type='Langlebig', design='aschig',
                                        function='Stadt', column_order=None,
                                        material='Stein', construction='Städtisch')
    building8 = Building.objects.create(name='Rosinen', city='Darmstadt',
                                        country='Deutschland', region='Hessen',
                                        era=klassik, architect='Laura Buhleier',
                                        context='Essen',
                                        builder='Quang Nguyen',
                                        construction_type='Gesund', design='schrumpelig',
                                        function='Ernährung', column_order=None,
                                        material='Trauben', construction='trocknen')
    building9 = Building.objects.create(name='TU', city='Darmstadt',
                                        country='Deutschland', region='Hessen',
                                        era=archaik, architect=None,
                                        context='Universität',
                                        builder='Ganesha Welsch',
                                        construction_type='Unterwürfig', design=None,
                                        function='Forschung', column_order='toskanisch',
                                        material='Stein', construction='Massivbau')
    building10 = Building.objects.create(name='Klingon', city=None,
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
    return frühzeit, archaik, römisch, klassik, hellenismus, \
           spätantike, sonstiges, building1, building2, building3, \
           building4, building5, building6, building7, building8, \
           building9, building10, building11


class DisplayTestCases(TestCase):
    """
    Testcases for the display_building function in view
    """

    def setUp(self):
        """
        Setting up a client, some buildings and eras for the tests
        """
        self.client = Client()

    def test1(self):
        """
        Testing building_filter function in views
        """
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 200)

    def test2_display_building_filter(self):
        """
        Test the display_building_function in views
        Testcase where there are no elements
        """
        response = self.client.get('/filter/')
        self.assertEqual(response.context['Cities'], [])
        self.assertEqual(response.context['Regions'], [])
        self.assertEqual(response.context['Countries'], [])
        self.assertEqual(response.context['Eras'], [])
        self.assertEqual(response.context['Architects'], [])
        self.assertEqual(response.context['Builders'], [])
        self.assertEqual(response.context['Designs'], [])
        self.assertEqual(response.context['Column_Orders'], [])
        self.assertEqual(response.context['Materials'], [])
        self.assertEqual(response.context['Functions'], [])
        self.assertEqual(response.context['Filter_Result'], [])
        self.assertEqual(response.context['Filter_Names'],
                         ['Stadt', 'Region', 'Land', 'Epoche', 'Architekt', 'Bauherr', 'Bauform',
                          'Säulenordnung', 'Material', 'Funktion'])
        self.assertEqual(response.context['Active_Filter'], {})

    def test3_display_building_filter_criteria(self):
        """
        Tests the display_building_function in views
        Testing if the context variable giving back the right criteria
        """
        era1, era2, era3, era4, era5, er6, era7, building1, \
        building2, building3, building4, building5, building6, \
        building8, building9, building9, building10, building11 = setup()
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['Cities']),
                             ['Berlin', 'Darmstadt', 'Istanbul', 'Köln', 'Paris', 'Pompeji', ])
        self.assertListEqual(list(response.context['Regions']),
                             ['Berlin', 'Hessen', 'Kampanien', 'Texas'])
        self.assertListEqual(list(response.context['Countries']),
                             ['China', 'Deutschland', 'Frankreich', 'Italien', 'Turkey', ])
        self.assertListEqual(list(response.context['Eras']),
                             ['Archaik', 'Frühzeit', 'Hellenismus', 'Klassik',
                              'Römische Kaiserzeit', 'Sonstiges', 'Spätantike'])
        self.assertListEqual(list(response.context['Architects']),
                             ['Jonas Günster', 'Jonathan Otto', 'Laura Buhleier', 'Manuel Singer',
                              'Philipp Krause', 'Simon Gröger', 'Spock', 'Winnie Puuh'])
        self.assertListEqual(list(response.context['Builders']),
                             ['Ganesha Welsch', 'Jonathan Otto', 'Michael Burnham',
                              'Michael Wendler', 'Philipp Krause', 'Quang Nguyen',
                              'Tebarts van Elst'])
        self.assertListEqual(list(response.context['Designs']),
                             ['Großartig', 'Prunk', 'aschig', 'erniedrigend',
                              'erstaunlich', 'neuartig', 'schrumpelig', 'tödlich'])
        self.assertListEqual(list(response.context['Column_Orders']),
                             ['dorisch', 'ionisch', 'klingonisch', 'komposite', 'toskanisch',
                              'vier'])
        self.assertListEqual(list(response.context['Materials']),
                             ['Marmor', 'Münzen', 'Planet', 'Stahl', 'Stein', 'Trauben', 'Ziegel'])
        self.assertListEqual(list(response.context['Functions']),
                             ['Denkmal', 'Destroy', 'Ernährung', 'Fegefeuer', 'Forschung',
                              'Heiligtum', 'Regierung', 'Stadt'])

    def test4_display_building_filter_results(self):
        """
        Tests the display_building_function in views
        Testcases with only one filter from every criteria at a time
        Also testing if the list in the context variable 'Active_Filter' is right
        """

        era1, era2, era3, era4, era5, er6, era7, building1, \
        building2, building3, building4, building5, building6, building7, \
        building8, building9, building10, building11 = setup()
        response = self.client.get('/filter/')
        response1 = self.client.get('/filter/?city=' + response.context['Cities'][0])
        response2 = self.client.get('/filter/?region=' + response.context['Regions'][0])
        response3 = self.client.get('/filter/?country=' + response.context['Countries'][0])
        response4 = self.client.get('/filter/?era=' + response.context['Eras'][0])
        response5 = self.client.get('/filter/?architect=' + response.context['Architects'][0])
        response6 = self.client.get('/filter/?builder=' + response.context['Builders'][0])
        response7 = self.client.get('/filter/?design=' + response.context['Designs'][0])
        response8 = self.client.get('/filter/?column_order=' + response.context['Column_Orders'][0])
        response9 = self.client.get('/filter/?material=' + response.context['Materials'][0])
        response10 = self.client.get('/filter/?function=' + response.context['Functions'][0])

        self.assertListEqual(list(response1.context['Filter_Result']),
                             [(building6, None), (building4, None), (building5, None),
                              (building1, None)])
        self.assertEqual(response1.context['Active_Filter'],
                         {'city': [response.context['Cities'][0]]})
        self.assertEqual(response1.status_code, 200)

        self.assertListEqual(list(response2.context['Filter_Result']),
                             [(building6, None), (building4, None), (building5, None),
                              (building3, None), (building1, None)])
        self.assertEqual(response2.context['Active_Filter'],
                         {'region': [response.context['Regions'][0]]})
        self.assertEqual(response2.status_code, 200)

        self.assertListEqual(list(response3.context['Filter_Result']),
                             [(building11, None)])
        self.assertEqual(response3.context['Active_Filter'],
                         {'country': [response.context['Countries'][0]]})
        self.assertEqual(response3.status_code, 200)

        self.assertListEqual(list(response4.context['Filter_Result']),
                             [(building3, None), (building9, None)])
        self.assertEqual(response4.context['Active_Filter'],
                         {'era': [response.context['Eras'][0]]})
        self.assertEqual(response4.status_code, 200)

        self.assertListEqual(list(response5.context['Filter_Result']),
                             [(building2, None)])
        self.assertEqual(response5.context['Active_Filter'],
                         {'architect': [response.context['Architects'][0]]})
        self.assertEqual(response5.status_code, 200)

        self.assertListEqual(list(response6.context['Filter_Result']),
                             [(building6, None), (building5, None), (building1, None),
                              (building9, None)])
        self.assertEqual(response6.context['Active_Filter'],
                         {'builder': [response.context['Builders'][0]]})
        self.assertEqual(response6.status_code, 200)

        self.assertListEqual(list(response7.context['Filter_Result']),
                             [(building3, None)])
        self.assertEqual(response7.context['Active_Filter'],
                         {'design': [response.context['Designs'][0]]})
        self.assertEqual(response7.status_code, 200)

        self.assertListEqual(list(response8.context['Filter_Result']),
                             [(building6, None), (building4, None), (building3, None)])
        self.assertEqual(response8.context['Active_Filter'],
                         {'column_order': [response.context['Column_Orders'][0]]})
        self.assertEqual(response8.status_code, 200)

        self.assertListEqual(list(response9.context['Filter_Result']),
                             [(building3, None)])
        self.assertEqual(response9.context['Active_Filter'],
                         {'material': [response.context['Materials'][0]]})
        self.assertEqual(response9.status_code, 200)

        self.assertListEqual(list(response10.context['Filter_Result']),
                             [(building2, None)])
        self.assertEqual(response10.context['Active_Filter'],
                         {'function': [response.context['Functions'][0]]})
        self.assertEqual(response10.status_code, 200)

    def test5_display_building_filter_results(self):
        """
        Tests the display_building_function in views
        Testcases with multiple filter criteria, only one from every criteria
        Also testing if the list in the context variable 'Active_Filter' is right
        """

        era1, era2, era3, era4, era5, er6, era7, building1, \
        building2, building3, building4, building5, building6, building7, \
        building8, building9, building10, building11 = setup()

        response = self.client.get('/filter/')
        response1 = self.client.get(
            '/filter/?city=' + response.context['Cities'][0]
            + '&region=' + response.context['Regions'][0]
            + '&country=' + response.context['Countries'][0]
            + '&era=' + response.context['Eras'][0]
            + '&architect=' + response.context['Architects'][0]
            + '&builder=' + response.context['Builders'][0]
            + '&design=' + response.context['Designs'][0]
            + '&column_order=' + response.context['Column_Orders'][0]
            + '&material=' + response.context['Materials'][0]
            + '&function=' + response.context['Functions'][0])
        # different order then before
        response2 = self.client.get(
            '/filter/?region=' + response.context['Regions'][0]
            + '&era=' + response.context['Eras'][0]
            + '&material=' + response.context['Materials'][0]
            + '&city=' + response.context['Cities'][0]
            + '&architect=' + response.context['Architects'][0]
            + '&country=' + response.context['Countries'][0]
            + '&design=' + response.context['Designs'][0]
            + '&column_order=' + response.context['Column_Orders'][0]
            + '&function=' + response.context['Functions'][0]
            + '&builder=' + response.context['Builders'][0])
        response3 = self.client.get(
            '/filter/?country=' + response.context['Countries'][0]
            + '&region=' + response.context['Regions'][0]
            + '&city=' + response.context['Cities'][0]
            + '&architect=' + response.context['Architects'][0]
            + '&builder=' + response.context['Builders'][0]
            + '&design=' + response.context['Designs'][0])
        response4 = self.client.get(
            '/filter/?function=' + response.context['Functions'][4]
            + '&material=' + response.context['Materials'][2]
            + '&era=' + response.context['Eras'][6])
        response5 = self.client.get(
            '/filter/?era=' + response.context['Eras'][1]
            + '&architect=' + response.context['Architects'][1])
        response6 = self.client.get(
            '/filter/?architect=' + response.context['Architects'][1]
            + '&era=' + response.context['Eras'][1])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.context['Filter_Result'],
                             [(building6, None),
                              (building4, None),
                              (building5, None),
                              (building2, None),
                              (building3, None),
                              (building10, None),
                              (building11, None),
                              (building7, None),
                              (building1, None),
                              (building8, None),
                              (building9, None)])
        self.assertEqual(response.context['Active_Filter'], {})

        self.assertListEqual(list(response1.context['Filter_Result']),
                             [])
        self.assertEqual(response1.context['Active_Filter'],
                         {'city': [response.context['Cities'][0]],
                          'region': [response.context['Regions'][0]],
                          'country': [response.context['Countries'][0]],
                          'era': [response.context['Eras'][0]],
                          'architect': [response.context['Architects'][0]],
                          'builder': [response.context['Builders'][0]],
                          'design': [response.context['Designs'][0]],
                          'column_order': [response.context['Column_Orders'][0]],
                          'material': [response.context['Materials'][0]],
                          'function': [response.context['Functions'][0]]})
        self.assertEqual(response1.status_code, 200)

        self.assertListEqual(list(response2.context['Filter_Result']),
                             [])
        self.assertEqual(response2.context['Active_Filter'],
                         {'city': [response.context['Cities'][0]],
                          'region': [response.context['Regions'][0]],
                          'country': [response.context['Countries'][0]],
                          'era': [response.context['Eras'][0]],
                          'architect': [response.context['Architects'][0]],
                          'builder': [response.context['Builders'][0]],
                          'design': [response.context['Designs'][0]],
                          'column_order': [response.context['Column_Orders'][0]],
                          'material': [response.context['Materials'][0]],
                          'function': [response.context['Functions'][0]]})
        self.assertEqual(response2.status_code, 200)

        self.assertListEqual(list(response3.context['Filter_Result']),
                             [])
        self.assertEqual(response3.context['Active_Filter'],
                         {'city': [response.context['Cities'][0]],
                          'region': [response.context['Regions'][0]],
                          'country': [response.context['Countries'][0]],
                          'architect': [response.context['Architects'][0]],
                          'builder': [response.context['Builders'][0]],
                          'design': [response.context['Designs'][0]]})
        self.assertEqual(response3.status_code, 200)

        self.assertListEqual(list(response4.context['Filter_Result']),
                             [])
        self.assertEqual(response4.context['Active_Filter'],
                         {'function': [response.context['Functions'][4]],
                          'material': [response.context['Materials'][2]],
                          'era': [response.context['Eras'][6]]})
        self.assertListEqual(list(response5.context['Filter_Result']),
                             [(building6, None), (building1, None)])
        self.assertEqual(response4.status_code, 200)

        self.assertEqual(response5.context['Active_Filter'],
                         {'era': [response.context['Eras'][1]],
                          'architect': [response.context['Architects'][1]]})
        self.assertEqual(response5.status_code, 200)

        self.assertListEqual(list(response6.context['Filter_Result']),
                             [(building6, None), (building1, None)])
        self.assertEqual(response6.context['Active_Filter'],
                         {'era': [response.context['Eras'][1]],
                          'architect': [response.context['Architects'][1]]})
        self.assertEqual(response6.status_code, 200)

        self.assertEqual(response5.context['Filter_Result'], response6.context['Filter_Result'])

    def test6_display_building_filter_results(self):
        """
        Testcases with multiple same filter criteria
        Also testing if the list in the context variable 'Active_Filter' is right
        """
        era1, era2, era3, era4, era5, er6, era7, building1, \
        building2, building3, building4, building5, building6, building7, \
        building8, building9, building10, building11 = setup()

        response = self.client.get('/filter/')
        response1 = self.client.get(
            '/filter/?architect=' + response.context['Architects'][1]
            + '&architect=' + response.context['Architects'][2]
            + '&architect=' + response.context['Architects'][3]
            + '&architect=' + response.context['Architects'][4]
            + '&architect=' + response.context['Architects'][5])
        response2 = self.client.get(
            '/filter/?city=' + response.context['Cities'][5]
            + '&era=' + response.context['Eras'][3]
            + '&city=' + response.context['Cities'][2]
            + '&era=' + response.context['Eras'][4])
        response3 = self.client.get(
            '/filter/?material=' + response.context['Materials'][4]
            + '&function=' + response.context['Functions'][4]
            + '&design=' + response.context['Designs'][4]
            + '&design=' + response.context['Designs'][3]
            + '&function=' + response.context['Functions'][6]
            + '&material=' + response.context['Materials'][1])
        response4 = self.client.get(
            '/filter/?design=' + response.context['Designs'][4]
            + '&material=' + response.context['Materials'][1]
            + '&function=' + response.context['Functions'][4]
            + '&design=' + response.context['Designs'][3]
            + '&material=' + response.context['Materials'][4]
            + '&function=' + response.context['Functions'][6])

        self.assertEqual(response.status_code, 200)

        self.assertListEqual(list(response1.context['Filter_Result']),
                             [(building6, None), (building4, None), (building5, None),
                              (building3, None), (building1, None), (building8, None)])
        self.assertEqual(response1.context['Active_Filter'],
                         {'architect': [response.context['Architects'][1],
                                        response.context['Architects'][2],
                                        response.context['Architects'][3],
                                        response.context['Architects'][4],
                                        response.context['Architects'][5]]})
        self.assertEqual(response1.status_code, 200)

        self.assertListEqual(list(response2.context['Filter_Result']),
                             [(building7, None)])
        self.assertEqual(response2.context['Active_Filter'],
                         {'city': [response.context['Cities'][5], response.context['Cities'][2]],
                          'era': [response.context['Eras'][3], response.context['Eras'][4]]})
        self.assertEqual(response2.status_code, 200)

        self.assertListEqual(list(response3.context['Filter_Result']),
                             [(building4, None), (building5, None), (building1, None)])
        self.assertEqual(response3.context['Active_Filter'],
                         {'material': [response.context['Materials'][4],
                                       response.context['Materials'][1]],
                          'function': [response.context['Functions'][4],
                                       response.context['Functions'][6]],
                          'design': [response.context['Designs'][4],
                                     response.context['Designs'][3]]})
        self.assertEqual(response3.status_code, 200)

        self.assertListEqual(list(response4.context['Filter_Result']),
                             [(building4, None), (building5, None), (building1, None)])
        self.assertEqual(response4.context['Active_Filter'],
                         {'design': [response.context['Designs'][4],
                                     response.context['Designs'][3]],
                          'material': [response.context['Materials'][1],
                                       response.context['Materials'][4]],
                          'function': [response.context['Functions'][4],
                                       response.context['Functions'][6]],
                          })
        self.assertEqual(response4.status_code, 200)

        self.assertEqual(response3.context['Filter_Result'], response4.context['Filter_Result'])


class FilterTestCases(TestCase):
    """
    Testcases for the my_filter, delete_duplicates, one_dict_set_to_string_list functions in view
    """
