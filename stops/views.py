from django.http import HttpResponse
from django.shortcuts import render
from stops.models import Stop
import requests
import json


def index(request):
    return HttpResponse("Hello, world. You're at the stops index.")

def populate(request):
    x = Stop()
    x.populate_db()
    result = Stop.objects.all().count()
    return HttpResponse(result)

def search_by_family(request):
    x = Stop()
    result = x.find_by_family("rrat")
    return render(request, 'stops/list.html', {'result': result})

def search_by_name_or_id(request):
    x = Stop()
    result = x.find_by_name_or_id("rat")
    return render(request, 'stops/list.html', {'result': result})

def show_all(request):
    all = Stop.objects.all()
    return render(request, 'stops/list.html', {'result': all})
