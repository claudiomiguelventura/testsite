# urls.py
from django.urls import path

from . import views

urlpatterns = [
path("", views.view, name="view"),
path("home/", views.home, name="home"),
path("create/", views.create, name="index"),
path("<int:id>", views.index, name="index"),
path("view/", views.view, name="view"),
path("<str:district>/<str:county>", views.show, name="show"),
]