"""
Configurations of the different functions and subpages from the App: start
"""

from django.shortcuts import render
# pylint: disable = import-error, no-name-in-module
from video_content.models import Video
from impressum.views import get_course_link
from django.http import HttpResponseRedirect


def login_required(f):
    """
    Decorator method for view-method to make sure a user is either logged in,
    or the user will redirected to /login (CAS Login).
    :param f: The function that requires a login, is decorated with this.
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
        return f(*args, **kwargs)
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
    video = Video.get_intro(Video)
    context = {
        'Video': video,
        'Kurs_Link': get_course_link(),
    }
    return render(request, 'start.html', context)
