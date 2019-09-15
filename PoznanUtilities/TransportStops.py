from datetime import datetime
from .DistanceCalculator import DistanceCalculator
from .UtilitiesAPIHandling import UtilitiesAPIHandling


class TransportStop:
    def __init__(self, lat, lon, name, id, lines):
        self.lines = lines
        self.name = name
        self.id = id
        self.lon = lon
        self.lat = lat
        self.distance_to = -1
        self.updated = 0

    def __str__(self):
        return "Współrzędne: {}, {}. Nazwa: {}, Linie: {}, Odległość: {} metrów, Ostatnia Aktualizacja {}"\
            .format(self.lon, self.lat, self.name, self.lines, self.distance_to, self.updated)

    def as_dict(self):
        transportstop_dict = dict()
        transportstop_dict['name'] = self.name
        transportstop_dict['id'] = self.id
        transportstop_dict['lines'] = " ".join(self.lines)
        transportstop_dict['lon'] = self.lon
        transportstop_dict['lat'] = self.lat
        transportstop_dict['distance_to'] = self.distance_to
        transportstop_dict['updated'] = self.updated
        return transportstop_dict


class TransportStops:
    def __init__(self):
        self.transportstops_data = []
        self.names = []
        self.load_transport_stop_data()

    def load_transport_stop_data_and_merge_similar_stops(self):
        # TODO move merging into a separate function

        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        transportstopjson = UtilitiesAPIHandling("stops", url)

        for transportstops in transportstopjson.get_json()['features']:
            if transportstops['properties']['stop_name'] not in self.names:
                lat = transportstops['geometry']['coordinates'][0]
                lon = transportstops['geometry']['coordinates'][1]
                name = transportstops['properties']['stop_name']
                id = transportstops['id']
                # 'headsigns' in the api is a string of line numbers, separated by comma and space
                lines = transportstops['properties']['headsigns'].replace(" ","").split(",")
                self.transportstops_data.append(TransportStop(lat, lon, name, id, lines))
                self.names.append(transportstops['properties']['stop_name'])
            else:
                #  Find stops with the same name, and in such case, only append the line numbers
                for transportstops_data_search in self.transportstops_data:
                    if transportstops_data_search.name == transportstops['properties']['stop_name']:
                        transportstops_data_search.lines.extend(transportstops['properties']['headsigns'].replace(" ","").split(","))
                        transportstops_data_search.lines = list(set(transportstops_data_search.lines))
                        transportstops_data_search.lines.sort()

    def load_transport_stop_data(self):
        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        transportstopjson = UtilitiesAPIHandling("stops", url)

        for transportstops in transportstopjson.get_json()['features']:
            lat = transportstops['geometry']['coordinates'][0]
            lon = transportstops['geometry']['coordinates'][1]
            name = transportstops['properties']['stop_name']
            id = transportstops['id']
            # 'headsigns' in the api is a string of line numbers, separated by comma and space
            lines = transportstops['properties']['headsigns'].replace(" ","").split(",")
            self.transportstops_data.append(TransportStop(lat, lon, name, id, lines))
            self.names.append(transportstops['properties']['stop_name'])     

    def find_transport_stop_distances(self, user_location):
        for transport_stop in self.transportstops_data:
            target_location = (transport_stop.lat, transport_stop.lon)
            transport_stop.distance_to = DistanceCalculator.get_distance(user_location, target_location, "greatcircle")
            transport_stop.updated = datetime.utcnow()

    def sort_transport_stops_by_distance(self):
        self.transportstops_data.sort(key=lambda x: x.distance_to)

    def get_transport_stops_data_as_dict(self, how_many=0):
        response = []
        if not how_many:
            for ts_data in self.transportstops_data:
                response.append(ts_data.as_dict())
        elif how_many > 0:
            for i in range(0, how_many):
                response.append(self.transportstops_data[i].as_dict())
        return {"response": response}

    def get_list_of_transport_stops_names(self):
        names = []
        for ts in self.transportstops_data:
            names.append(ts.name)
        return names

    def get_list_of_transport_stops_ids(self):
        ids = []
        for ts in self.transportstops_data:
            ids.append(ts.id)
        return ids
