from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os

@login_required
def mainView(request):
    return render(request, "index.html")

def store_file(file, filename, user):
   name = user.username + "/" + filename
   os.makedirs(os.path.dirname(name), exist_ok=True)
   with open(name, "wb") as f:
       f.write(file.read())

@csrf_exempt
@login_required
def uploadView(request):
    if request.method == "POST":
        user = request.user
        file = request.FILES['file']
        filename = request.POST.get("name")
        store_file(file, filename, user)
        return redirect("/")

    return render(request, "upload.html")
