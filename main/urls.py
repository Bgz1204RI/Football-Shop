# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("",views.about, name="home"),
    path("about/", views.about, name="about"),
]
