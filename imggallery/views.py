from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import os

@login_required
def mainView(request):
    pictures = []
    try:
        pictures = list(os.listdir(request.user.username))
    except:
        pass
    return render(request, "index.html", {"pictures": pictures, "username": request.user.username})

def store_file(file, filename, user):
   username = user.username
   os.system("mkdir -p " + username)
   os.system("touch " + username + "/" + filename)
   with open(username + "/" + filename, "wb") as f:
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

@login_required
def getImageView(request):
    filename = request.GET.get("filename")
    with open(request.user.username + "/" + filename, "rb") as f:
        filedata = f.read()
        return HttpResponse(filedata, content_type="image")
    return redirect("/")

def adminPanelView(request):
    if request.POST.get("password") == "hardcoded":
        pictures = []
        usernames = [user.username for user in get_user_model().objects.all()]
        for user in usernames:
            try:
                pictures += list(os.listdir(request.user.username))
            except:
                pass
        return render(request, "admin.html", {"pictures": pictures})
    else:
        return HttpResponse("Incorrect password")

def adminLoginView(request):
    return render(request, "adminlogin.html")
