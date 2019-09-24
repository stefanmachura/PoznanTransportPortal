from .UtilitiesAPIHandling import UtilitiesAPIHandling
from .DistanceCalculator import DistanceCalculator
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

    def search_for_stops(self, query, merging=True):
        result = []
        known_families = []
        for stop in self.transportstops_data:
            if (query.lower() in stop['name'].lower()) or (query.lower() in stop['id'].lower()):
                if not merging:
                    result.append(stop)
                else:
                    if stop['family'] not in known_families:
                        result.append(stop)
                        known_families.append(stop['family'])
        return result

    def find_stops(self, query):
        result = []
        for stop in self.transportstops_data:
            if query.lower() in stop['name'].lower():
                result.append(stop)
        for stop in self.transportstops_data:
            if query.lower() in stop['id'].lower():
                result.append(stop)
        return result

    def get_stop_location(self, stops):
        # TODO: ogarnąć to
        lats = []
        lons = []
        result = None
        for stop in stops:
            lats.append(stop['lat'])
            lons.append(stop['lon'])
        final_lat = sum(lats) / len(lats)
        final_lon = sum(lons) / len(lons)
        return (final_lat, final_lon)

    def load_transport_stop_data(self):
        self.load_stop_data_from_api()

        for transportstops in self.transportstops_json.get_json()['features']:
            lat = transportstops['geometry']['coordinates'][0]
            lon = transportstops['geometry']['coordinates'][1]
            name = transportstops['properties']['stop_name']
            id = transportstops['id']
            # family is a common id for a group of stops with the same name, eg. FRRY 41, and FRRY42 are of FRRY family
            family = transportstops['id'][:-2]
            # 'headsigns' in the api is a string of line numbers, separated by comma and space
            lines = transportstops['properties']['headsigns'].replace(" ", "").split(",")
            self.transportstops_data.append({'lat': lat, 'lon': lon, 'name': name, 'id': id, 'family': family, 'lines': lines})

    def find_transport_stop_distances(self, user_location):
        for transport_stop in self.transportstops_data:
            target_location = (transport_stop.lat, transport_stop.lon)
            transport_stop['distance_to'] = DistanceCalculator.get_distance(user_location, target_location, "greatcircle")
            transport_stop['distance_updated'] = datetime.utcnow()

    def sort_transport_stops_by_distance(self):
        self.transportstops_data.sort(key=lambda x: x.distance_to)
