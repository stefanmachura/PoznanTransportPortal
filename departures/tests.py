from django.test import TestCase
from stops.models import Stop
from .models import Departure


import datetime
import pytz


class TestDepartureModel(TestCase):
    def setUp(self):
        local_timezone = pytz.timezone('Europe/Warsaw')

        test_line = '9'
        test_headsign = 'Piątkowska'
        test_timestamp = datetime.datetime.strptime("24.10.2019 - 23:00", "%d.%m.%Y - %H:%M")
        test_timestamp = local_timezone.localize(test_timestamp)
        test_tram_stop = Stop.objects.create(latitude='52', longitude='16', name='Testowiec', given_id='TEST42', family='TEST', lines='1,2,5')

        Departure.objects.create(line=test_line, headsign=test_headsign, timestamp=test_timestamp, stop=test_tram_stop)

        test_line2 = '16'
        test_headsign2 = 'Piątkowska'
        test_timestamp2 = datetime.datetime.strptime("25.10.2019 - 01:00", "%d.%m.%Y - %H:%M")
        test_timestamp2 = local_timezone.localize(test_timestamp2)
        test_tram_stop2 = Stop.objects.create(latitude='52.3', longitude='16.1', name='Testowo', given_id='TEST43', family='TEST', lines='2,4,9')

        Departure.objects.create(line=test_line2, headsign=test_headsign2, timestamp=test_timestamp2, stop=test_tram_stop2)

        test_line3 = '16'
        test_headsign3 = 'Franowo'
        test_timestamp3 = datetime.datetime.strptime("25.10.2019 - 01:10", "%d.%m.%Y - %H:%M")
        test_timestamp3 = local_timezone.localize(test_timestamp3)
        test_tram_stop3 = Stop.objects.create(latitude='52.3', longitude='16.1', name='Testowo', given_id='TEST43', family='TEST', lines='2,4,9')

        Departure.objects.create(line=test_line3, headsign=test_headsign3, timestamp=test_timestamp3, stop=test_tram_stop3)

        test_line4 = '1'
        test_headsign4 = 'Starołęka'
        test_timestamp4 = datetime.datetime.strptime("26.10.2019 - 18:50", "%d.%m.%Y - %H:%M")
        test_timestamp4 = local_timezone.localize(test_timestamp4)
        test_tram_stop4 = Stop.objects.create(latitude='52.3', longitude='16.1', name='Testowo', given_id='TEST43', family='TEST2', lines='2,4,9')

        Departure.objects.create(line=test_line4, headsign=test_headsign4, timestamp=test_timestamp4, stop=test_tram_stop4)

        test_line5 = '1'
        test_headsign5 = 'Starołęka'
        test_timestamp5 = datetime.datetime.strptime("20.10.2019 - 11:30", "%d.%m.%Y - %H:%M")
        test_timestamp5 = local_timezone.localize(test_timestamp5)
        test_tram_stop5 = Stop.objects.create(latitude='52.3', longitude='16.1', name='Testowo', given_id='TEST43', family='TEST2', lines='2,4,9')

        Departure.objects.create(line=test_line5, headsign=test_headsign5, timestamp=test_timestamp5, stop=test_tram_stop5)

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

        dep = Departure.objects.get(line='16', headsign='Piątkowska')

        self.assertEqual(dep.get_wait_time(current_time), 180)

    def test_finding_future_deps_of_stop_family(self):
        error, result = Departure.objects.get_departures('TEST2')
        self.assertEqual(result.count(), 1)

    def test_getting_departures_error_message(self):
        error, result = Departure.objects.get_departures('NONE')
        self.assertEqual(error, "error")
        self.assertEqual(result, None)

    def test_loading_departures(self):
        result = Departure.objects.load_departures('TEST')
        self.assertEqual(result, ['TEST42', 'TEST43', 'TEST43'])
