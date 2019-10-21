from django.test import TestCase
from .models import Stop

class StopModelTests(TestCase):

    def test_api_connect(self):
        x = Stop()
        c = x.connect()
        self.assertEqual(c.status_code, 200)

    def test_api_data_format_correct(self):
        x = Stop()
        x.connect()
        j = x.get_api_json()
        self.assertTrue('features' in j)

    def test_searching_by_family(self):
        Stop.objects.create(latitude="51",
                            longitude="42",
                            name="Fredry1",
                            given_id="FRRY41",
                            family="FRRY",
                            lines="1,2,3,4,5")
        Stop.objects.create(latitude="11",
                            longitude="22",
                            name="Fredry2",
                            given_id="FRRY61",
                            family="FRRY",
                            lines="1,2,3,4,5")                   
        x = Stop()
        result = x.find_by_family("FRRY")
        self.assertEqual(len(result), 2)

    def test_searching_by_name_and_id(self):
        Stop.objects.create(latitude="51",
                            longitude="42",
                            name="frydry",
                            given_id="x",
                            family="FRRY",
                            lines="1,2,3,4,5")
        Stop.objects.create(latitude="11",
                            longitude="22",
                            name="x",
                            given_id="FRRY61",
                            family="FRRY",
                            lines="1,2,3,4,5")                   
        x = Stop()
        result = x.find_by_name_or_id("ry")
        self.assertEqual(len(result), 2)
    