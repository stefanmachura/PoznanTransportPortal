from datetime import datetime
from calendar import monthrange
import json
from .UtilitiesAPIHandling import UtilitiesAPIHandling
from .TransportStops import TransportStops


def weekday_to_number(weekday):
    weekdays = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
    return weekdays.index(weekday)


class TransportDepartures:
    def __init__(self):
        self.list_of_departures = []
        self.api_data = []
        self.stops = None

    def load_stops(self, stops):
        self.stops = stops

    def get_api_data(self):
        for stop in self.stops:
            url = "http://www.poznan.pl/mim/komunikacja/service.html?stop_id=" + stop['id']
            data = UtilitiesAPIHandling(stop['id'], url)
            self.api_data.append(data.get_json())

    def generate_departures_list(self):
        self.get_api_data()

        for data in self.api_data:
            lines = data["routes"]
            # TODO change this so that it read the time from API
            my_time = datetime.now()

            for line in lines:
                headsign = line['variants'][0]['headsign']
                upcoming_days_timetables = line['variants'][0]['services']

                for timetable in upcoming_days_timetables:
                    day_delta = abs(my_time.weekday() - weekday_to_number(timetable["when"]))
                    if day_delta >= 6:
                        day_delta -= 5
                    """
                    in the timetable it is provided for which day it is, so we need to calculate the day delta, e.g.
                    how many days in the future is the day of the timetable
                    """
                    for trips in timetable['departures']:
                        try:
                            departure_time = datetime(my_time.year, my_time.month, my_time.day + day_delta, int(trips["hours"]), int(trips["minutes"]))
                        except ValueError:
                            departure_time = datetime(my_time.year, my_time.month + 1, (my_time.day + day_delta) - monthrange(my_time.year, my_time.month + 1)[1], int(trips["hours"]), int(trips["minutes"]))
                        time_until_departure = departure_time - my_time
                        time_until_departure_in_minutes = int(time_until_departure.total_seconds()) // 60

                        self.list_of_departures.append({"line": line["name"], "headsign": headsign, "departure_time": departure_time.strftime("%H:%M"), "tud": time_until_departure_in_minutes})

        self.list_of_departures = sorted(self.list_of_departures, key=lambda k: k['tud'])

    def get_list_of_departures(self):
        return self.list_of_departures
