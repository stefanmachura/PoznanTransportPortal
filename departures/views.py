from django.shortcuts import render
from django.http import HttpResponse
from .models import Departure


# Create your views here.
def index(request):
    Departure.objects.load_departures('RRAT')
    return HttpResponse("Hello departures!")
