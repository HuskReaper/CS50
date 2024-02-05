from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def request(request):
    return HttpResponse("This is a request in django.")

def example(request):
    return HttpResponse("This is an example of a HTTPResponse in django.")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")