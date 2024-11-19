from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def mainView(request):
    return render(request, "index.html")

@login_required
def uploadView(request):
    return render(request, "upload.html")
