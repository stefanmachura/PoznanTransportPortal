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