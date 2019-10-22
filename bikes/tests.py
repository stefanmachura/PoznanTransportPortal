from django.test import TestCase
from .models import BikeRack

class BikeModelTest(TestCase):

    def test_api_connect(self):
        x = BikeRack()
        c = x.connect()
        self.assertEqual(c.status_code, 200)

    def test_api_data_format_correct(self):
        x = BikeRack()
        x.connect()
        j = x.get_api_json()
        self.assertTrue('features' in j)

    def test_data_loading(self):
        x = BikeRack()
        result = x.get_data_from_api()
        self.assertEqual(len(result), 137)

    # def test_populating(self):
    #     bikeracks = BikeRack()
    #     bikeracks.populate()
    #     self.assertEqual(bikeracks.objects.all().count(), 137)

