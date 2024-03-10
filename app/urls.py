from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("pilotage", views.pilotage, name="pilotage"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("configurationgtb", views.configurationgtb, name="configurationgtb"),
    path("visualisation", views.visualisation, name="visualisation"),
    path("planification", views.planification, name="planification"),



]