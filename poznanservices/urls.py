from django.urls import path
from poznanservices import views

urlpatterns = [
    path("", views.search, name="search"),
    path("timetable/", views.timetable, name="timetable"),
]