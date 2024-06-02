from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search_entry, name="search"),
    path("new/", views.new_entry, name="new"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("random/", views.random_page, name="randompage")
]
