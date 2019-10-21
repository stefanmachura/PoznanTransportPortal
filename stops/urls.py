from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("populate/", views.populate, name="save"),
    path("search/", views.search_by_family, name="search_f"),
    path("search2/", views.search_by_name_or_id, name="search_nid"),
    path("show/", views.show_all, name="show")
]