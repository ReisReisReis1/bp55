"""
Configurations of the different viewable functions and subpages from the App: home
"""

from django.shortcuts import render


def index(request):
    """
    Subpage to index (first site appearing after someone opens the website)
    :param request: url request to get subpage /
    :return: rendering the subpage based on index.html
    """
    return render(request, 'home/index.html')
