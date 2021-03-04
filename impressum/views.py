"""
Configurations of the Website subpages from the App: impressum
"""

from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from .models import Impressum


def get_course_link():
    try:
        first_object = Impressum.objects.all().first()
        if first_object is None:
            return ''
        else:
            link = first_object.course_link
            return link
    except Impressum.DoesNotExist:
        return ''



def impressum(request):
    """
    Subpage to show the impressum and the moodle_link
    :param request: url request to get impressum
    :return: rendering the subpage based on impressum.html
    with a context variable to get the characteistics
    """

    context = {
        'Kurs_Link': get_course_link()
    }
    return render(request, "impressum.html", context)