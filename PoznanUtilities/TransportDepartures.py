from datetime import datetime
from calendar import monthrange
import json
from .UtilitiesAPIHandling import UtilitiesAPIHandling
from .NaturalLanguage import natural_time
from .TransportStops import TransportStops


def weekday_to_number(weekday):
    weekdays = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
    return weekdays.index(weekday)


class TransportDepartures:
    def __init__(self, stop="FRRY41"):
        self.list_of_departures = []
        self.api_data = None
        self.stop = stop
        self.get_api_data()
        self.determine_input_type()

    def determine_input_type(self):
        if self.stop[-2:].isdigit():
            self.get_api_data()
            self.generate_departures_list()
        else:
            ts = TransportStops()
            applicable_stops = []
            list_of_stops = ts.get_list_of_transport_stops_ids()
            for stop_id in list_of_stops:
                if self.stop == stop_id[:-2]:
                    applicable_stops.append(stop_id)
            print(applicable_stops)
            for ast in applicable_stops:
                self.stop = ast
                self.get_api_data()
                self.generate_departures_list()

    def as_JSON(self):
        return json.dumps(self.list_of_departures[0:3])

    def get_tram_departures_data_as_dict(self, how_many=0):
        response = []
        if not how_many:
            for ts_data in self.list_of_departures:
                response.append(ts_data)
        elif how_many > 0:
            for i in range(0, how_many):
                response.append(self.list_of_departures[i])
        return {"response": response}

    def generate_departures_list(self):
        lines = self.api_data["routes"]
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
                        departure_time = datetime(my_time.year, my_time.month, my_time.day + day_delta,
                                                  int(trips["hours"]), int(trips["minutes"]))
                    except ValueError:
                        departure_time = datetime(my_time.year, my_time.month + 1,
                                                  (my_time.day + day_delta) -
                                                  monthrange(my_time.year, my_time.month + 1)[1],
                                                  int(trips["hours"]), int(trips["minutes"]))

                    time_until_departure = departure_time - my_time
                    time_until_departure_in_minutes = int(time_until_departure.total_seconds()) // 60

                    self.list_of_departures.append(
                        {"line": line["name"], "headsign": headsign, "departure_time": departure_time.strftime("%H:%M"),
                         "tud": time_until_departure_in_minutes})

        self.list_of_departures = sorted(self.list_of_departures, key=lambda k: k['tud'])

    def get_api_data(self):
        url = "http://www.poznan.pl/mim/komunikacja/service.html?stop_id=" + self.stop
        data = UtilitiesAPIHandling(self.stop, url)
        self.api_data = data.get_json()

    def print_list_of_departures(self):
        for lot in self.list_of_departures:
            print(lot)

    def get_list_of_departures(self):
        return self.list_of_departures

    def get_nice_list_of_departures(self, linebreak):
        result = ""
        for lot in self.list_of_departures:
            result += lot["line"] + " odjazd " + lot["departure_time"] + " za " + natural_time(lot["tud"]) + linebreak
        return result
