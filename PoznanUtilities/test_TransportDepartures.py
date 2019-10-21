import unittest
from PoznanUtilities import TransportDepartures, TransportStops


class TestDepartures(unittest.TestCase):

    def test_data_loading(self):
        td = TransportDepartures.TransportDepartures()
        ts = TransportStops.TransportStops()
        ts.load_transport_stop_data()
        x = ts.search_for_stops_by_query("FRRY41", merging=False)
        td.load_stops(x)
        td.get_api_data()
        self.assertTrue(td.api_data)

    def test_departures_generation(self):
        td = TransportDepartures.TransportDepartures()
        ts = TransportStops.TransportStops()
        ts.load_transport_stop_data()
        x = ts.search_for_stops_by_query("FRRY41", merging=False)
        td.load_stops(x)
        td.get_api_data()
        td.generate_departures_list()
        self.assertTrue(td.list_of_departures)

    def test_getting_departures_list(self):
        td = TransportDepartures.TransportDepartures()
        ts = TransportStops.TransportStops()
        ts.load_transport_stop_data()
        x = ts.search_for_stops_by_query("FRRY41", merging=False)
        td.load_stops(x)
        td.get_api_data()
        td.generate_departures_list()
        self.assertTrue(td.get_list_of_departures())
