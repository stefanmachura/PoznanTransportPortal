from django.shortcuts import render
from django.http import HttpResponse
from .models import Departure


# Create your views here.
def index(request):
    return HttpResponse("Hello departures!")
