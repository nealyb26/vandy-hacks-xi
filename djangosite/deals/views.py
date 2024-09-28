from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("This is the homepage for the deals app!")