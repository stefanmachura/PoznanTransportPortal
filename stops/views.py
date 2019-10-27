from django.http import HttpResponse
from django.shortcuts import render
from stops.models import Stop
import requests
import json


def index(request):
    return HttpResponse("Hello, world. You're at the stops index.")
