from django.test import TestCase
from stops.models import Stop
from .models import Departure


import datetime
import pytz


class TestDepartureModel(TestCase):
    def setUp(self):
        test_line = '9'
        test_headsign = 'Piątkowska'
        test_timestamp = datetime.datetime.strptime("24.10.2019 - 23:00", "%d.%m.%Y - %H:%M")
        local_timezone = pytz.timezone('Europe/Warsaw')
        test_timestamp = local_timezone.localize(test_timestamp)
        test_tram_stop = Stop.objects.create(latitude='52', longitude='16', name='Testowiec', given_id='TEST42', family='TEST', lines='1,2,5')

        Departure.objects.create(line=test_line, headsign=test_headsign, timestamp=test_timestamp, stop=test_tram_stop)

        test_line2 = '16'
        test_headsign2 = 'Piątkowska'
        test_timestamp2 = datetime.datetime.strptime("25.10.2019 - 01:00", "%d.%m.%Y - %H:%M")
        local_timezone = pytz.timezone('Europe/Warsaw')
        test_timestamp2 = local_timezone.localize(test_timestamp2)
        test_tram_stop2 = Stop.objects.create(latitude='52', longitude='16', name='Testowiec', given_id='TEST42', family='TEST', lines='1,2,5')

        Departure.objects.create(line=test_line2, headsign=test_headsign2, timestamp=test_timestamp2, stop=test_tram_stop2)

    def test_wait_calculation(self):
        current_time = datetime.datetime.strptime("24.10.2019 - 22:00", "%d.%m.%Y - %H:%M")

        local_timezone = pytz.timezone('Europe/Warsaw')
        current_time = local_timezone.localize(current_time)

        dep = Departure.objects.get(line='9')

        self.assertEqual(dep.get_wait_time(current_time), 60)

    def test_wait_calculation_for_tomorrow(self):
        current_time = datetime.datetime.strptime("24.10.2019 - 22:00", "%d.%m.%Y - %H:%M")

        local_timezone = pytz.timezone('Europe/Warsaw')
        current_time = local_timezone.localize(current_time)

        dep = Departure.objects.get(line='16')

        self.assertEqual(dep.get_wait_time(current_time), 180)
