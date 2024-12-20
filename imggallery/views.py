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
    if os.name == "nt": # Making sure it works on windows as well
        username = user.username
        os.system("mkdir " + username)
        # Fix for flaw 2:
        # uncomment the two lines below
        # if not filename.isalpha():
        #     return
        os.system("copy NUL " + username + "\\" + filename)
        with open(username + "\\" + filename, "wb") as f:
            f.write(file.read())
    else:
        username = user.username
        os.system("mkdir -p " + username)
        # Fix for flaw 2:
        # uncomment the two lines below
        # if not filename.isalpha():
        #     return
        os.system("touch " + username + "/" + filename)
        with open(username + "/" + filename, "wb") as f:
            f.write(file.read())

# Fix for flaw 4:
# remove @csrf_exempt
# also check templates/upload.html for a fix
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
    if os.name == "nt": # Making sure it works on windows as well
        filepath = request.user.username + "\\" + filename
    else:
        filepath = request.user.username + "/" + filename
    # Fix for flaw 1:
    # uncomment the six lines below
    # if os.name == "nt": # Windows fix
    #     if not os.path.abspath(filepath).startswith(os.getcwd() + "\\" + request.user.username):
    #         return redirect("/")
    # else:
    #     if not os.path.abspath(filepath).startswith(os.getcwd() + "/" + request.user.username):
    #         return redirect("/")
    if os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            filedata = f.read()
            return HttpResponse(filedata, content_type="image")
    return redirect("/")

# @login_required
def adminPanelView(request):
    # Fix for flaw 3:
    # replace the if statement in the code with the one commented out below
    # also uncomment the @login_required above this function
    # if request.user.username == "root":
    if request.POST.get("password") == "hardcoded":
        pictures = []
        usernames = [user.username for user in get_user_model().objects.all()]
        for user in usernames:
            try:
                pictures += list(os.listdir(user))
            except:
                pass
        return render(request, "admin.html", {"pictures": pictures})
    else:
        return HttpResponse("Incorrect password")

def adminLoginView(request):
    return render(request, "adminlogin.html")
