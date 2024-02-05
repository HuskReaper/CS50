from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("request", views.request, name="request"),
    path("example", views.example, name="example"),
    path("<str:name>", views.greet, name="greet")
]