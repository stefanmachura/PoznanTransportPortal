from django.db import models, IntegrityError
from stops.models import Stop

import datetime
import requests
import pytz


class DepartureManager(models.Manager):
    def add_departures(self, stop_id):
        url = "http://www.poznan.pl/mim/komunikacja/service.html?stop_id=" + stop_id
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

                        # when the timetable goes over midnight, the 'when' in API changes to next day, and we need to add a day to the departure timestamp
                        if today != when:
                            timestamp += datetime.timedelta(days=1)

                        # making the timestamp tz aware so that timedelta can be calculated
                        local_timezone = pytz.timezone('Europe/Warsaw')
                        timestamp = local_timezone.localize(timestamp)

                        utc_timestamp = timestamp.astimezone(pytz.utc)

                        new_departure = Departure(line=line, headsign=headsign, timestamp=utc_timestamp, stop=Stop.objects.get(given_id=stop_id))
                        try:
                            new_departure.save()
                        except IntegrityError:
                            # do nothing if this departure alredy exists
                            pass

    def load_departures(self, family):
        stops = [x.given_id for x in Stop.objects.find_by_family(family)]
        for stop in stops:
            Departure.objects.add_departures(stop)
        return stops

    def get_departures(self, query):
        now = datetime.datetime.utcnow()
        local_timezone = pytz.timezone('UTC')
        tz_now = local_timezone.localize(now)
        result = Departure.objects.filter(timestamp__gte=tz_now).filter(stop__family=query)
        if result.count() == 0:
            self.load_departures(query)
            result = Departure.objects.filter(timestamp__gte=tz_now).filter(stop__family=query)
            if result.count() == 0:
                return "error", None
            else:
                return None, result
        else:
            return None, result


class Departure(models.Model):
    line = models.CharField(max_length=10)
    headsign = models.CharField(max_length=30)
    timestamp = models.DateTimeField()
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    objects = DepartureManager()

    class Meta:
        ordering = ["timestamp"]
        constraints = [
            models.UniqueConstraint(fields=['line', 'headsign', 'timestamp'], name='unique_departure'),
        ]

    def __str__(self):
        return "{} {} {} {}".format(self.line, self.headsign, datetime.datetime.strftime(self.timestamp, "%d.%m.%Y - %H:%M"), self.stop.given_id)

    def get_wait_time(self, current_time):
        delta = self.timestamp - current_time
        return delta.total_seconds() // 60
