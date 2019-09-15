from django.shortcuts import render
from django.http import HttpResponse
from PoznanUtilities import TransportDepartures
from PoznanUtilities import TransportStops
from PoznanUtilities import BikeRacks


def search(request):
        return render(request, 'poznanservices/search.html', {})


def timetable(request):
        stop = request.GET.get('stop')
        td = TransportDepartures.TransportDepartures()
        td.find_applicable_stops(stop)
        td.generate_departures_list()
        list_of_departures = td.get_list_of_departures()

        ts = TransportStops.TransportStops()
        ts.load_transport_stop_data()
        location = ts.get_stop_location(stop)
        print(location)

        br = BikeRacks.BikeRacks()
        br.find_bikerack_distances(location)
        br.sort_bikeracks_by_distance()
        bikes = br.get_racks_data_as_dict(5)

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
                if departure['line'] == unique_destination[0] and departure['headsign'] == unique_destination[1] and departure['tud'] < 800 and departure['tud'] > 0:
                    unique_destination_timetable["departures"].append((departure['departure_time'], departure['tud']))
            if len(unique_destination_timetable["departures"]) > 0:
                lines_timetables.append(unique_destination_timetable)

        lines_timetables = sorted(lines_timetables, key=lambda k: k['desc'][0])
        return render(request, 'poznanservices/timetable.html', {'timetables': lines_timetables, 'bikes': bikes})
