from django.shortcuts import render
from django.http import HttpResponse
from PoznanUtilities import TransportDepartures
from PoznanUtilities import TransportStops
from PoznanUtilities import BikeRacks
import os

from stops.models import Stop


def search(request):
        if 'stop' not in request.POST:
            return render(request, 'poznanservices/search.html', {})
        else:
            # ts = TransportStops.TransportStops()
            # ts.load_transport_stop_data()
            # result = ts.search_for_stops_by_query(request.POST['stop'], merging=True)

            ts = Stop()
            result = ts.find_by_name_or_id(request.POST['stop'], True)


            if not result:
                return render(request, 'poznanservices/search.html', {"error": "Nie znaleziono przystanku"})
            else:
                return render(request, 'poznanservices/search.html', {"q": result})


def timetable(request):
        stop = request.GET.get('stop')


        ss = Stop()
        location = ss.get_location_of_stop_family(stop)

        ts = TransportStops.TransportStops()
        ts.load_transport_stop_data()
        sss = ts.search_for_stops_by_family(stop)

        td = TransportDepartures.TransportDepartures()
        td.load_stops(sss)
        td.generate_departures_list()
        list_of_departures = td.get_list_of_departures()

        br = BikeRacks.BikeRacks()
        br.find_bikerack_distances(location)
        br.sort_bikeracks_by_distance()
        bikes = br.get_racks_data_as_dict(5)
        # TODO: errors for bike system and stops system
        # TODO: unit tests for error system

        if td.error_code == 1:
            error_message = "System ZTM nie zwrócił żadnych danych, spróbuj ponownie za jakiś czas"
            return render(request, 'poznanservices/timetable.html', {'error_message': error_message, 'bikes': bikes})
            
        else:
            unique_destinations = []
            lines_timetables = []

            for departure in list_of_departures:
                if not (departure['line'], departure['headsign']) in unique_destinations:
                    unique_destinations.append((departure['line'], departure['headsign']))

            for unique_destination in unique_destinations:
                unique_destination_timetable = {}
                unique_destination_timetable["desc"] = unique_destination
                unique_destination_timetable["departures"] = []
                for departure in list_of_departures:
                    if departure['line'] == unique_destination[0] and departure['headsign'] == unique_destination[1] and (0 < departure['tud'] < 60):
                        unique_destination_timetable["departures"].append((departure['departure_time'], departure['tud']))
                del unique_destination_timetable["departures"][5:]
                if len(unique_destination_timetable["departures"]) > 0:
                    lines_timetables.append(unique_destination_timetable)
            lines_timetables = sorted(lines_timetables, key=lambda k: k['desc'][0])
            return render(request, 'poznanservices/timetable.html', {'timetables': lines_timetables, 'error': error_message, 'bikes': bikes})



def show_logs(request):
    files = os.listdir('PoznanUtilitiesData')
    return render(request, 'poznanservices/logs.html', {'files': files})


def show_single_log(request, fname):
    with open('PoznanUtilitiesData\\' + fname, "r") as log_file:
        log = log_file.read()
    return HttpResponse(log.replace('\n', '<br/>'))
