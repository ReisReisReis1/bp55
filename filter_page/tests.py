"""
Tests for functions in the App: home
"""
# pylint: disable=all


from django.test import Client, TestCase
# pylint: disable=import-error
from model_bakery import baker
from details_page.models import Building, Era


def setup(self):
    """
    Setting up some test data
    """
    self.frühzeit = Era.objects.create(name='Frühzeit')
    self.archaik = Era.objects.create(name='Archaik')
    self.hellenismus = Era.objects.create(name='Helenismus')
    self.römisch = Era.objects.create(name='Römische Kaiserzeit')
    self.klassik = Era.objects.create(name='Klassik')
    self.spätantike = Era.objects.create(name='Spätantike')
    self.sonstiges = Era.objects.create(name='Sonstiges')

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
    return self.frühzeit, self.archaik, self.römisch, self.klassik, self.hellenismus, \
           self.spätantike, self.sonstiges, self.building1, self.building2, self.building3, \
           self.building4, self.building5, self.building6, self.building7, self.building8, \
           self.building9, self.building10, self.building1self.building11


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
