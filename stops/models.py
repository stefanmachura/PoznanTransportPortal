from django.db import models
from django.db.models import Q

import requests


class StopManager(models.Manager):

    def find_by_family(self, query):
        result = Stop.objects.filter(family__exact=query.upper())
        return result

    def get_location_of_stop_family(self, query):
        stops = Stop.objects.find_by_family(query)
        lats = []
        lons = []
        for stop in stops:
            lats.append(float(stop.latitude))
            lons.append(float(stop.longitude))
        lat = sum(lats) / len(lats)
        lon = sum(lons) / len(lons)
        return (lat, lon)


class Stop(models.Model):
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    given_id = models.CharField(max_length=20)
    family = models.CharField(max_length=20)
    lines = models.CharField(max_length=50)

    objects = StopManager()

    def __str__(self):
        return f"{self.name} - {self.given_id}"

    def len(self):
        return Stop.objects.all().count()

    def connect(self):
        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        return requests.get(url)

    def get_api_json(self):
        api_data = self.connect()
        return api_data.json()

    def find_by_name_or_id(self, query, distinct=False):
        result = Stop.objects.filter(Q(name__icontains=query) | Q(given_id__icontains=query))
        # a not-so-nice way to simulate SQL distinct keyword on single column
        if distinct:
            families = []
            distinct_result = []
            for r in result:
                if r.family not in families:
                    distinct_result.append(r)
                    families.append(r.family)
                else:
                    continue
            return distinct_result
        else:
            return result

    def populate_db(self, how_many=0):
        api_data = self.connect()
        stops = api_data.json()
        for s in stops["features"]:
            new_stop = Stop(latitude=s['geometry']['coordinates'][0],
                            longitude=s['geometry']['coordinates'][1],
                            name=s['properties']['stop_name'],
                            given_id=s['id'],
                            family=s['id'][:-2],
                            lines=s['properties']['headsigns'].replace(" ", ""))
            new_stop.save()
