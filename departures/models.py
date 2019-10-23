from django.db import models
from stops.models import Stop

import datetime
import requests
import pytz


class DepartureManager(models.Manager):
    def add_departures(self):
        x = "SWLE42"
        url = "http://www.poznan.pl/mim/komunikacja/service.html?stop_id=" + x
        r = requests.get(url)
        r.encoding = "utf-8"
        data = r.json()

        today = data['date'].split(", ")  # splitting the date provided in the api to Polish weekday name and the proper date that can be parsed
        for route in data['routes']:
            line = route['name']
            variants = route['variants']
            for variant in variants:
                headsign = variant['headsign']
                for service in variant['services']:
                    when = service['when']
                    departures = []
                    for departure in service['departures']:
                        hour = departure['hours']
                        if len(hour) == 1:  # hours in the api response are not zero-padded :(
                            hour = "0" + hour

                        # generating a datetime object with time and date of departure
                        time = today[1] + " - " + hour + ":" + departure['minutes']
                        timestamp = datetime.datetime.strptime(time, "%d.%m.%Y - %H:%M")

                        # making the timestamp tz aware so that timedelta can be calculated
                        local_timezone = pytz.timezone('Europe/Warsaw')
                        timestamp = local_timezone.localize(timestamp)

                        new_departure = Departure(line=line, headsign=headsign, timestamp=timestamp, stop=Stop.objects.get(given_id=x))
                        new_departure.save()


class Departure(models.Model):
    line = models.CharField(max_length=10)
    headsign = models.CharField(max_length=30)
    timestamp = models.DateTimeField()
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    objects = DepartureManager()

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return "{} {} {} {}".format(self.line, self.headsign, datetime.datetime.strftime(self.timestamp, "%d.%m.%Y - %H:%M"), self.stop.given_id)

    def get_wait_time(self, current_time):
        delta = self.timestamp - current_time
        return delta.total_seconds() // 60
