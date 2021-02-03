"""
Tests for functions in the App: home
"""
# pylint: disable=all


from django.test import Client, TestCase
# pylint: disable=import-error
from model_bakery import baker
from details_page.models import Building, Era
from filter_page.views import one_dict_set_to_string_list, delete_duplicates, my_filter


def setup():
    """
    Setting up some test data
    """
    frühzeit = Era.objects.create(name='Frühzeit')
    archaik = Era.objects.create(name='Archaik')
    hellenismus = Era.objects.create(name='Helenismus')
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
                                        country='Frankreich', region='',
                                        era=römisch, architect='Jonas Günster',
                                        context='Weltausstellung',
                                        builder='Michael Wendler',
                                        construction_type='groß', design='erstaunlich',
                                        function='Denkmal', column_order='vier',
                                        material='Stahl', construction='')
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
                                        construction_type='Erhaben', design='Erniedrigend',
                                        function='Regierung', column_order='dorisch',
                                        material='Stein', construction='Massivbau')
    building5 = Building.objects.create(name='Bundestag', city='Berlin',
                                        country='Deutschland', region='Berlin',
                                        era=hellenismus, architect='Simon Gröger',
                                        context='Regierungsgebäude',
                                        builder='Ganesha Welsch',
                                        construction_type='Erhaben', design='erniedrigend',
                                        function='Regierung', column_order='ionisch',
                                        material='Ziegel', construction='Massivbau')
    building6 = Building.objects.create(name='Alexander Platz', city='Berlin',
                                        country='Deutschland', region='Berlin',
                                        era=frühzeit, architect='Jonathan Otto',
                                        context='Regierungsgebäude',
                                        builder='Ganesha Welsch',
                                        construction_type='Platzartig', design='neuartig',
                                        function='Regierung', column_order='dorisch',
                                        material='Stein', construction='Massivbau')
    building7 = Building.objects.create(name='Pompeji', city='Pompeji',
                                        country='Italien', region='Kampanien',
                                        era=römisch, architect='',
                                        context='Historische Stadt',
                                        builder='',
                                        construction_type='Langlebig', design='aschig',
                                        function='Stadt', column_order='',
                                        material='Stein', construction='Städtisch')
    building8 = Building.objects.create(name='Rosinen', city='Darmstadt',
                                        country='Deutschland', region='Hessen',
                                        era=klassik, architect='Laura Buhleier',
                                        context='Essen',
                                        builder='Quang Ngyuen',
                                        construction_type='Gesund', design='schrumpelig',
                                        function='Ernährung', column_order='',
                                        material='Trauben', construction='trocknen')
    building9 = Building.objects.create(name='TU', city='Darmstadt',
                                        country='Deutschland', region='Hessen',
                                        era=archaik, architect='',
                                        context='Universität',
                                        builder='Ganesha Welsch',
                                        construction_type='Unterwürfig', design='',
                                        function='Forschung', column_order='toskanisch',
                                        material='Stein', construction='Massivbau')
    building10 = Building.objects.create(name='Klingon', city='',
                                         country='', region='',
                                         era=spätantike, architect='Spock ',
                                         context='Planet der Klingonen',
                                         builder='Michael Burnham',
                                         construction_type='', design='tödlich',
                                         function='Desytroy', column_order='klingonisch',
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
        self.test1 = baker.make('details_page.Building')
        self.test2 = baker.make('details_page.Building')
        self.test3 = baker.make('details_page.Building')
        self.test4 = baker.make('details_page.Building')
        self.test5 = baker.make('details_page.Building')

    def test1(self):
        """
        Testing building_filter function in views
        """
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 200)


class FilterTestCases(TestCase):
    """
    Testcases for the my_filter, delete_duplicates, one_dict_set_to_string_list functions in view
    """

    def test_one_dict_set_to_string_list(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Era.objects.values("name")
        str_list = ['Frühzeit', 'Archaik', 'Helenismus', 'Römische Kaiserzeit', 'Klassik',
                    'Spätantike', 'Sonstiges']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list2(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("country")
        str_list = ['Deutschland', 'Frankreich', 'Turkey', 'Deutschland', 'Deutschland',
                    'Deutschland', 'Italien', 'Deutschland', 'Deutschland', '', 'China']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list3(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("region")
        str_list = ['Berlin', '', 'Berlin', 'Berlin', 'Berlin', 'Berlin', 'Kampanien', 'Hessen',
                    'Hessen', '', 'Texas']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list4(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("city")
        str_list = ['Berlin', 'Paris', 'Istanbul', 'Berlin', 'Berlin', 'Berlin', 'Pompeji',
                    'Darmstadt', 'Darmstadt', '', 'Köln']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list5(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("architect")
        str_list = ['Jonathan Otto', 'Jonas Günster', 'Manuel Singer', 'Philipp Krause',
                    'Simon Gröger', 'Jonathan Otto', '', 'Laura Buhleier', '', 'Spock ',
                    'Winnie Puuh']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list6(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("builder")
        str_list = ['Ganesha Welsch', 'Michael Wendler', 'Philipp Krause', 'Jonathan Otto',
                    'Ganesha Welsch', 'Ganesha Welsch', '', 'Quang Ngyuen', 'Ganesha Welsch',
                    'Michael Burnham', 'Tebarts van Elst']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list7(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("column_order")
        str_list = ['ionisch', 'vier', 'dorisch', 'dorisch', 'ionisch', 'dorisch', '', '',
                    'toskanisch', 'klingonisch', 'komposite']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list8(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("design")
        str_list = ['erniedrigend', 'erstaunlich', 'Großartig', 'Erniedrigend', 'erniedrigend',
                    'neuartig', 'aschig', 'schrumpelig', '', 'tödlich', 'Prunk']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list9(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("material")
        str_list = ['Stein', 'Stahl', 'Marmor', 'Stein', 'Ziegel', 'Stein', 'Stein', 'Trauben',
                    'Stein', 'Planet', 'Münzen']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_one_dict_set_to_string_list10(self):
        """
        This tests the one_dict_set_to_string_list method.
        """
        setup()
        dict_lst = Building.objects.values("function")
        str_list = ['Regierung', 'Denkmal', 'Heiligtum', 'Regierung', 'Regierung', 'Regierung',
                    'Stadt', 'Ernährung', 'Forschung', 'Desytroy', 'Fegefeuer']
        self.assertEqual(one_dict_set_to_string_list(dict_lst), str_list)

    def test_delete_duplicates1(self):
        """
        Tests for the delete duplicates helper method. Tests different data types.
        :return: None
        """
        lst = [1, 2, 3, 4, 5, 6]
        lst_wod = lst
        self.assertListEqual(delete_duplicates(lst), lst_wod)

    def test_delete_duplicates2(self):
        """
        Tests for the delete duplicates helper method. Tests different data types.
        :return: None
        """
        lst = []
        lst_wod = lst
        self.assertListEqual(delete_duplicates(lst), lst_wod)

    def test_delete_duplicates3(self):
        """
        Tests for the delete duplicates helper method. Tests different data types.
        :return: None
        """
        lst = [1, 1, 2, 3, 3, 4, 5]
        lst_wod = [1, 2, 3, 4, 5]
        self.assertListEqual(delete_duplicates(lst), lst_wod)

    def test_delete_duplicates4(self):
        """
        Tests for the delete duplicates helper method. Tests different data types.
        :return: None
        """
        lst = ["1", "1"]
        lst_wod = ["1"]
        self.assertListEqual(delete_duplicates(lst), lst_wod)

    def test_delete_duplicates5(self):
        """
        Tests for the delete duplicates helper method. Tests different data types.
        :return: None
        """
        lst = [[1, 2, 3], [1, 2, 3], [4, 5], [4, 5]]
        lst_wod = [[1, 2, 3], [4, 5]]
        self.assertListEqual(delete_duplicates(lst), lst_wod)

    def test_delete_duplicates6(self):
        """
        Tests for the delete duplicates helper method. Tests different data types.
        :return: None
        """
        data = setup()
        lst = [data[4], data[2], data[4], data[3], data[0], data[4]]
        lst_wod = [data[4], data[2], data[3], data[0]]
        self.assertListEqual(delete_duplicates(lst), lst_wod)

    def test_delete_duplicates7(self):
        """
        Tests for the delete duplicates helper method. Tests different data types.
        :return: None
        """
        lst = ["1", 2, [1, 2], ["1", "2"], (7, 8), 0.9]
        lst_wod = lst
        self.assertListEqual(delete_duplicates(lst), lst_wod)

    def test_my_filter_empty(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "GIBT ES NICHT"
        value = "Frühzeit"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(era__name=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_unfiltered))

    def test_my_filter_era(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "era"
        value = "Frühzeit"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(era__name=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_country(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "country"
        value = "Deutschland"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(country__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_region(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "region"
        value = "Hessen"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(region__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_city(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "city"
        value = "Darmstadt"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(city__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_architect(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "architect"
        value = "Jonathan"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(architect__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_builder(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "builder"
        value = "Quang"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(builder__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_columnorder(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "column_order"
        value = "ionisch"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(column_order__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_design(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "design"
        value = "EIN DESIGN FÜR DAS MAL NICHTS GEFUNDEN WIRD"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(design__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_material(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "material"
        value = "Münzen"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(material__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

    def test_my_filter_function(self):
        """
        Test the my_filter helper
        :return: None
        """
        setup()
        key = "function"
        value = "Regierung"
        qs_unfiltered = Building.objects.all()
        qs_filtered = qs_unfiltered.filter(function__icontains=value)
        self.assertListEqual(list(my_filter(qs_unfiltered, key, value)), list(qs_filtered))

