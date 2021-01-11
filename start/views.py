"""
Configurations of the different viewable functions and subpages from the App: start
"""


from django.shortcuts import render
# pylint: disable = import-error, no-name-in-module
from video_content.models import Video


# Create your views here.


def start(request):
    """
    Subpage start
    :param request: url request to get subpage /start
    :return: rendering the subpage based on start.html
    with a context variable to get the intro-video
    """
    video = Video.get_intro(Video)
    context = {
        'video': video
    }
    return render(request, 'start.html', context)
