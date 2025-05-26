from django.urls import path
from . import views

app_name = "hello"
urlpatterns = [
    path("", views.index, name="index"),
    path("request", views.request, name="request"),
    path("example", views.example, name="example"),
]