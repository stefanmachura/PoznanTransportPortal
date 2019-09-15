import unittest
from PoznanUtilities import TransportDepartures


class TestDepartures(unittest.TestCase):

    def test_data_loading(self):
        td = TransportDepartures.TransportDepartures()
        td.find_applicable_stops("FRRY")
        td.get_api_data()
        self.assertTrue(td.api_data)

    def test_stops_finding(self):
        td = TransportDepartures.TransportDepartures()
        td.find_applicable_stops("FRRY")
        self.assertEqual(len(td.stops), 2)

    def test_departures_generation(self):
        td = TransportDepartures.TransportDepartures()
        td.find_applicable_stops("FRRY")
        td.generate_departures_list()
        self.assertTrue(td.list_of_departures)

    def test_getting_departures_list(self):
        td = TransportDepartures.TransportDepartures()
        td.find_applicable_stops("FRRY")
        td.generate_departures_list()
        self.assertTrue(td.get_list_of_departures)
