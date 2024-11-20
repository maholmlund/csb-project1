from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainView, name='mainView'),
    path("upload/", views.uploadView, name="uploadView"),
    path("getimage/", views.getImageView, name="getImageView"),
    path("adminpanel/", views.adminPanelView, name="adminPanelView"),
    path("adminlogin/", views.adminLoginView, name="adminLoginView"),
]
