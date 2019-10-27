from django.test import TestCase
from .models import Stop


class StopModelTests(TestCase):
    def setUp(self):
        Stop.objects.create(latitude="10",
                            longitude="10",
                            name="frydry",
                            given_id="x",
                            family="FRRY",
                            lines="1,2,3,4,5")
        Stop.objects.create(latitude="20",
                            longitude="20",
                            name="x",
                            given_id="FRRY61",
                            family="FRRY",
                            lines="1,2,3,4,5")

    def test_location_calculation(self):
        self.assertEqual((15, 15), Stop.objects.get_location_of_stop_family('FRRY'))

    def test_search_by_family(self):
        result = Stop.objects.find_by_family("frry").count()
        self.assertEqual(result, 2)

    def search_by_name_or_id(self):
        result = Stop.objects.find_by_name_or_id("rat")
        self.assertEqual(result.given_id, 'FRRY61')
