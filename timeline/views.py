"""
Configurations of the different viewable functions and subpages from the App: timeline
"""


from django.shortcuts import render
from details_page import models

# Create your views here.


def timeline(request):
    """
    Subpage "Zeitstrahl"
    :param request: url request to get subpage /timeline
    :return: rendering the subpage based on timeline.html
    """
    return render(request, 'timeline.html')
