from django.shortcuts import render
from django.http import HttpResponse

def mainView(request):
    return HttpResponse("Test site")
