from django.shortcuts import render
from video_content.models import Videos
# Create your views here.

# Definition auf Index mit Rückgabe auf index.html
def index(request):
    return render(request, 'home/index.html')


def start(request):
    #Path to the Intro Video
    video = Videos.objects.get(title='VL_Archaik-1-3')
    context = {
        'video': video
    }
    return render(request, 'home/start.html', context)


def zeitstrahl(request):
    return render(request, 'home/zeitstrahl.html')


def themengrid(request):
    return render(request, 'home/themengrid.html')


def t(request):
    return render(request, 'home/t.html')


def header(request):
    return render(request, 'home/header.html')
