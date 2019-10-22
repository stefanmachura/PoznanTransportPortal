from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("update", views.update, name="up"),
    path("populate", views.populate, name="save"),
]