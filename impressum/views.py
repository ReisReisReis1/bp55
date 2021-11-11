"""
Configurations of the Website subpages from the App: impressum
"""

from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from .models import Impressum
from announcements.views import get_announcements


def get_course_link():
    """
    Getting the link to the moodle course
    """
    link = ''
    first_object = Impressum.objects.all()
    if first_object.first() is not None and first_object.first().course_link is not None:
        link = first_object.first().course_link
    return link


def impressum(request):
    """
    Subpage to show the impressum and the moodle_link
    :param request: url request to get impressum
    :return: rendering the subpage based on impressum.html
    with a context variable to get the characteistics
    """

    context = {
        'Kurs_Link': get_course_link(),
        'announcements': get_announcements(),
    }
    return render(request, "impressum.html", context)
