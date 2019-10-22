from django.http import HttpResponse
from django.shortcuts import render
from .models import BikeRack

def index(request):
    br = BikeRack()
    return HttpResponse("hejka")

def populate(request):
    br = BikeRack()
    br.populate()
    return HttpResponse("Baza stworzona")

def update(request):
    br = BikeRack()
    br.update()
    return HttpResponse("Baza rowerów została zaktualizowana")