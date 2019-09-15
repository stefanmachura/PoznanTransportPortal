from UtilitiesAPIHandling import UtilitiesAPIHandling
from DistanceCalculator import DistanceCalculator
import datetime


class TransportStops:
    def __init__(self):
        self.transportstops_data = []
        self.transportstops_json = None
        self.error_message = ""
        self.error_code = 0

    def load_stop_data_from_api(self):
        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        try:
            self.transportstops_json = UtilitiesAPIHandling("stops", url)
        except:
            self.error_message = "Could not load data from API"
            self.error_code = 1

    def find_stop_by_id(self, query):
        result = []
        for stop in self.transportstops_data:
            if query in stop['id']:
                result.append(stop)
        return result

    def find_stop_by_name(self, query):
        result = []
        for stop in self.transportstops_data:
            if query in stop['name']:
                result.append(stop)
        return result

    def load_transport_stop_data(self):
        for transportstops in self.transportstops_json.get_json()['features']:
            lat = transportstops['geometry']['coordinates'][0]
            lon = transportstops['geometry']['coordinates'][1]
            name = transportstops['properties']['stop_name']
            id = transportstops['id']
            # 'headsigns' in the api is a string of line numbers, separated by comma and space
            lines = transportstops['properties']['headsigns'].replace(" ", "").split(",")
            self.transportstops_data.append({'lat': lat, 'lon': lon, 'name': name, 'id': id, 'lines': lines})

    def find_transport_stop_distances(self, user_location):
        for transport_stop in self.transportstops_data:
            target_location = (transport_stop.lat, transport_stop.lon)
            transport_stop['distance_to'] = DistanceCalculator.get_distance(user_location, target_location, "greatcircle")
            transport_stop['distance_updated'] = datetime.utcnow()

    def sort_transport_stops_by_distance(self):
        self.transportstops_data.sort(key=lambda x: x.distance_to)
