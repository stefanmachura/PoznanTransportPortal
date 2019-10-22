from django.shortcuts import render
from django.http import HttpResponse

import os
import requests
import datetime
import json

from stops.models import Stop
from bikes.models import BikeRack

def create_departures_list(request):
    urls = []
    data = []
    ss = Stop()
    stops = ss.find_by_name_or_id("Rataje")
    for stop in stops:
        urls.append("http://www.poznan.pl/mim/komunikacja/service.html?stop_id=" + stop.given_id + "<br/>")
        url = "http://www.poznan.pl/mim/komunikacja/service.html?stop_id=" + stop.given_id
        r = requests.get(url)
        r.encoding = 'utf-8'
        data.append(r.json())
    return HttpResponse(data)


def search(request):
        if 'stop' not in request.POST:
            return render(request, 'poznanservices/search.html', {})
        else:
            ts = Stop()
            result = ts.find_by_name_or_id(request.POST['stop'], True)
            if not result:
                return render(request, 'poznanservices/search.html', {"error": "Nie znaleziono przystanku"})
            else:
                return render(request, 'poznanservices/search.html', {"q": result})


def timetable(request):
    stop = request.GET.get('stop')

    # TODO: errors for bike system and stops system
    # TODO: unit tests for error system
        
    stops = Stop()
    sss = stops.find_by_family(stop)

    td = TransportDepartures.TransportDepartures()
    td.load_stops(sss)
    td.generate_departures_list()
    list_of_departures = td.get_list_of_departures()

    br = BikeRack()
    bikes = br.find_nearest((17, 52))

    if td.error_code == 1:
        error_message = "System ZTM nie zwrócił żadnych danych, spróbuj ponownie za jakiś czas"
        return render(request, 'poznanservices/timetable.html', {'error_message': error_message, 'bikes': bikes})
    else:
        return render(request, 'poznanservices/timetable.html', {'timetables': list_of_departures, 'error': error_message, 'bikes': bikes})

def mock(request):
    destinations = []
    some_time_ago =  datetime.datetime.strptime("24.09.2019 - 00:00", "%d.%m.%Y - %H:%M")

    with open("WOPO01_JSON.txt", "r") as json_file:
        data = json.load(json_file)
        today = data['date'].split(", ") # splitting the date provided in the api to Polish weekday name and the proper date that can be parsed
        for route in data['routes']:
            name = route['name']
            variants = route['variants']
            for variant in variants:
                headsign = variant['headsign']
                for service in variant['services']:
                    when = service['when']
                    departures = []                    
                    for departure in service['departures']:
                        hour = departure['hours']
                        if len(hour) == 1: # hours in the api response are not zero-padded :(
                            hour = "0" + hour

                        # generating a datetime object with time and date of departure
                        time = today[1] + " - " + hour + ":" + departure['minutes']
                        timestamp = datetime.datetime.strptime(time, "%d.%m.%Y - %H:%M")

                        if today[0] != when: # this is when a part of the timetable goes past midnight to the next day
                            timestamp += datetime.timedelta(days=1)
                        delta = timestamp - some_time_ago 
                        departures.append({'time': timestamp, 'desc': departure['trip_desc'], 'delta': int(delta.total_seconds() / 60)})
                        departures = sorted(departures, key=lambda k: k['delta'])
                destinations.append({'name': name, 'headsign': headsign, 'departures': departures[0:10]})

    br = BikeRack()
    bikes = br.find_nearest((17, 52))
    return render(request, 'poznanservices/timetable.html', {'timetables': destinations, 'error': None, 'bikes': bikes})
