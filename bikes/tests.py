from django.test import TestCase
from .models import BikeRack


class BikeModelTest(TestCase):
    def test_api_connect(self):
        x = BikeRack.objects.connect()
        self.assertEqual(x.status_code, 200)

    def test_api_data_format_correct(self):
        x = BikeRack.objects.get_api_json()
        self.assertTrue('features' in x)
