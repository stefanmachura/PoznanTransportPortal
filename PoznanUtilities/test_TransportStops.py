import unittest
from PoznanUtilities import TransportStops


class TestStops(unittest.TestCase):

    def test_data_loading(self):
        ts = TransportStops.TransportStops()
        ts.load_stop_data_from_api()
        self.assertTrue(ts.transportstops_json)

    def test_data_ingestions(self):
        ts = TransportStops.TransportStops()
        ts.load_stop_data_from_api()
        ts.load_transport_stop_data()
        self.assertTrue(ts.transportstops_data)

    def test_searching_for_stop_with_exact_id(self):
        ts = TransportStops.TransportStops()
        ts.load_stop_data_from_api()
        ts.load_transport_stop_data()
        x = ts.find_stop_by_id("FRRY41")
        self.assertEqual(len(x), 1)

    def test_searching_for_stop_with_blurry_id(self):
        ts = TransportStops.TransportStops()
        ts.load_stop_data_from_api()
        ts.load_transport_stop_data()
        x = ts.find_stop_by_id("FRRY")
        self.assertEqual(len(x), 2)

    def test_searching_for_nonexisting_id(self):
        ts = TransportStops.TransportStops()
        ts.load_stop_data_from_api()
        ts.load_transport_stop_data()
        x = ts.find_stop_by_id("LOL22")
        self.assertEqual(len(x), 0)

    def test_searching_for_stop_with_good_name(self):
        ts = TransportStops.TransportStops()
        ts.load_stop_data_from_api()
        ts.load_transport_stop_data()
        x = ts.find_stop_by_name("Fredry")
        self.assertEqual(len(x), 2)

    def test_searching_for_stop_with_wrong_name(self):
        ts = TransportStops.TransportStops()
        ts.load_stop_data_from_api()
        ts.load_transport_stop_data()
        x = ts.find_stop_by_name("LOL")
        self.assertEqual(len(x), 0)
