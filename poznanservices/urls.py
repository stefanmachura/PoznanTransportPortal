from django.urls import path
from poznanservices import views

urlpatterns = [
    path("", views.search, name="search"),
    path("timetable/", views.timetable, name="timetable"),
    path("testing/", views.create_departures_list, name="l"),
    path("mock/", views.mock, name="mock")
]