from django.shortcuts import render
from django.http import HttpResponse

from stops.models import Stop
from bikes.models import BikeRack
from departures.models import Departure


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
    stop_of_departures = request.GET.get('stop')

    # TODO: errors for bike system and stops system
    # TODO: code cleanup
    # TODO: unit tests
    # TODO: prepare mock content
    # TODO: Error handling
    # TODO: db cleaning of old departures

    error_message, departures = Departure.objects.get_departures(stop_of_departures)
    family_name = Stop.objects.filter(family=stop_of_departures)[0]

    location = Stop.objects.get_location_of_stop_family(stop_of_departures)

    br = BikeRack()
    bikes = br.find_nearest(location)

    return render(request, 'poznanservices/timetable.html', {'departures': departures[:10], 'error_message': error_message, 'bikes': bikes, 'name': family_name.name})
