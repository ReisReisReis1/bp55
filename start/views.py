"""
Configurations of the different functions and subpages from the App: start
"""

from django.shortcuts import render
# pylint: disable = import-error, no-name-in-module
from video_content.models import Video
from impressum.views import get_course_link


def start(request):
    """
    Subpage start
    :param request: url request to get subpage /start
    :return: rendering the subpage based on start.html
    with a context variable to get the intro-video
    """
    video = Video.get_intro(Video)
    context = {
        'Video': video,
        'Kurs_Link': get_course_link(),
    }
    return render(request, 'start.html', context)
