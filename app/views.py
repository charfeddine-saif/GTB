from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, 'app/home.html')


def login(request):
    return render(request, 'app/login.html')



def pilotage(request):
    return render(request, 'app/pilotage.html')


def dashboard(request):
    return render(request, 'app/dashboard.html')


def configurationgtb(request):
    return render(request, 'app/configurationgtb.html')

def visualisation(request):
    return render(request, 'app/visualisation.html')

def planification(request):
    return render(request, 'app/planification.html')