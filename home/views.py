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


def header(request):
    """
    The header of every site of the webpage excluding the homesite
    :param request: requesting to render the header
    :return: rendering the header on the site based on header.html
    """
    return render(request, 'home/header.html')
