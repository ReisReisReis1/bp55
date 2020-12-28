"""
Configurations of the Website subpages from the App: home
"""

from django.shortcuts import render
# pylint: disable = import-error, no-name-in-module
from video_content.models import Videos
# Create your views here.



def index(request):
    """
    Subpage to index (first site appearing after someone opens the website)
    :param request: url request to subpage /
    :return: rendering the subpage based on index.html
    """
    return render(request, 'home/index.html')


def start(request):
    """
    Subpage start
    :param request: url request to subpage /start
    :return: rendering the subpage based on start.html
    """
    # pylint: disable = no-member
    video = Videos.objects.get(title='VL_Archaik-1-3')
    context = {
        'video': video
    }
    return render(request, 'home/start.html', context)


def zeitstrahl(request):
    """
    Subpage "Zeitstrahl"
    :param request: url request to subpage /timeline
    :return: rendering the subpage based on zeitstrahl.html
    """
    return render(request, 'home/zeitstrahl.html')


def themengrid(request):
    """
    Subpage "Gebäudefilter"
    :param request: url request to subpage /themengrid
    :return: rendering the subpage based on themengrid.html
    """
    return render(request, 'home/themengrid.html')


def header(request):
    """
    The header of every site of the webpage excluding the homesite
    :param request: requesting to render the header
    :return: rendering the header on the site based on header.html
    """
    return render(request, 'home/header.html')
