"""
Configurations of the Website subpages from the App: impressum
"""

from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from .models import Impressum


def get_course_link():
    first_object = Impressum.objects.all().first()
    link = first_object.course_link
    # return impressum.first_object
    return link



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
