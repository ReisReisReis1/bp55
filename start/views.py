"""
Configurations of the different functions and subpages from the App: start
"""

from django.shortcuts import render
from django.http import HttpResponseRedirect
# pylint: disable = import-error, no-name-in-module
from video_content.models import Video
from .models import IntroTexts
from impressum.views import get_course_link
from announcements.views import get_announcements
from analytics.views import register_visit


def login_required(func):
    """
    Decorator method for view-method to make sure a user is either logged in,
    or the user will redirected to /login (CAS Login).
    :param func: The function that requires a login, is decorated with this.
    :return: The wrapper function which than will decide what to do.
    """
    def wrapper(*args, **kwargs):
        """
        Inner function to decide what the upper decorator should do.
        Core is to aks if user is logged in.
        :param args: Arguments of the decorated function.
        :param kwargs: Listed Arguments of the decorated function.
        :return: Either the view function if user is logged in, otherwise a
        HttpResponseRedirect to /login (CAS Login).
        """
        request = args[0]
        # If the current user is not logged in: Redirect to /login.
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login")
        return func(*args, **kwargs)
    return wrapper


# Hier einkommentieren für SSO
#@login_required
def start(request):
    """
    Subpage start
    :param request: url request to get subpage /start
    :return: rendering the subpage based on start.html
    with a context variable to get the intro-video
    """
    register_visit(request, "Introseite")
    texts = IntroTexts.objects.all()
    intro_text = ""
    timeline_card_text = ""
    buildings_card_text = ""
    video_card_text = ""
    if texts.first() is not None:
        intro_text = texts.first().intro_text
        timeline_card_text = texts.first().timeline_card_text
        buildings_card_text = texts.first().buildings_card_text
        video_card_text = texts.first().video_card_text
    video = Video.get_intro(Video)
    context = {
        'Video': video,
        'intro_text': intro_text,
        'timeline_card_text': timeline_card_text,
        'buildings_card_text': buildings_card_text,
        'video_card_text': video_card_text,
        'Kurs_Link': get_course_link(),
        'announcements': get_announcements(),
    }
    return render(request, 'start.html', context)
