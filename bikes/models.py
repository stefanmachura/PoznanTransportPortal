from django.db import models
import requests
import datetime
import pytz
from haversine import haversine

class BikeRack(models.Model):
    api_id = models.IntegerField(default=0)
    free_bikes = models.IntegerField(default=0)
    free_racks = models.IntegerField(default=0)
    name = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now_add=True)
    updated.editable = True
    objects = models.Manager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


    def connect(self):
        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=stacje_rowerowe"
        return requests.get(url)
    
    def get_api_json(self):
        api_data = self.connect()
        return api_data.json()

    def get_data_from_api(self):
        api_data = self.get_api_json()
        result = []
        for bike_rack in api_data['features']:
            time = datetime.datetime.strptime(bike_rack['properties']['updated'], "%Y-%m-%d %H:%M")
            result.append({'api_id': bike_rack['id'],
            'free_racks': bike_rack['properties']['free_racks'],
            'free_bikes': bike_rack['properties']['bikes'],
            'name': bike_rack['properties']['label'],
            'longitude': bike_rack['geometry']['coordinates'][0],
            'latitude':bike_rack['geometry']['coordinates'][1],
            'updated': time
            })
        return result


    def populate(self):
        data = self.get_api_json()
        for bike_rack in data['features']:
            time = datetime.datetime.strptime(bike_rack['properties']['updated'], "%Y-%m-%d %H:%M")

            new_br = BikeRack(api_id=bike_rack['id'],
                              free_racks=bike_rack['properties']['free_racks'],
                              free_bikes=bike_rack['properties']['bikes'],
                              name=bike_rack['properties']['label'],
                              longitude=bike_rack['geometry']['coordinates'][0],
                              latitude=bike_rack['geometry']['coordinates'][1],
                              updated=time)
            new_br.save()
        return "OK"

    def update(self):
        fresh_data = self.get_data_from_api()
        tz = pytz.timezone('Europe/Warsaw')
        # I know one should never store timezone aware times, but this app is written specifically for one specific city, so we should be ok
        for fd in fresh_data:
            try:
                my_rack = BikeRack.objects.get(api_id=fd['api_id'])
                my_rack.free_bikes = fd['free_bikes']
                my_rack.updated = datetime.datetime.now(tz)
                my_rack.save()
            except:
                continue

    def find_nearest(self, user_location):
        located = []
        results = BikeRack.objects.all()
        for result in results:
            result_dict = result.__dict__
            bike_rack_location = (float(result.longitude), float(result.latitude))
            distance = int(haversine(user_location, bike_rack_location, unit='m'))
            result_dict['distance_to'] = distance
            located.append(result_dict)
        located.sort(key=lambda x: x['distance_to'])
        return located[:5]

