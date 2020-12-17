from django.shortcuts import render


# Create your views here.

# Definition auf Index mit Rückgabe auf index.html
def index(request):
    return render(request, 'home/index.html')


def start(request):
    return render(request, 'home/start.html')


def zeitstrahl(request):
    return render(request, 'home/zeitstrahl.html')


def themengrid(request):
    return render(request, 'home/themengrid.html')


def t(request):
    return render(request, 'home/t.html')


def header(request):
    return render(request, 'home/header.html')
