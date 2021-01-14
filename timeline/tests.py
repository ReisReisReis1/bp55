"""
Tests for functions in the App: timeline
"""
from django.test import TestCase
from timeline.models import HistoricDate
from details_page.models import Era


class HistoricDatesTests(TestCase):
    def setUp(self) -> None:
        # For each test
        Era.object.create(name="Test", year_from=9, year_from_BC_or_AD="n.Chr.", year_to=10, year_to_BC_or_AD="n.Chr.")
        HistoricDate.objects.create(year=1, year_BC_or_AD="v.Chr.", title="-1 vor Jesus", infos="Test 1",
                                    era=Era.objects.filter(name="Test").id)
        #HistoricDate.objects.create(year=1, year_BC_or_AD="n.Chr.", title="1 nach Jesus", infos="Test 2", era=None)
        #HistoricDate.objects.create(year=2, year_BC_or_AD="n.Chr.", title="2 nach Jesus", infos="Test 3", era=None)

    def setUpTestData(self):
        # For all tests in common
        pass

    def tearDown(self) -> None:
        # useless, cause TestCase will handle tearDown for database stuff
        pass

    def test_getYearAsSignedInt(self):
        #self.assertEqual(HistoricDate.objects.get(title="-1 vor Jesus").getYearAsSignedInt(), -1)
        pass
