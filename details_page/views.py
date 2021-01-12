"""
Configurations of the different viewable functions and subpages from the App: details_page
"""

from django.shortcuts import render


def detailed(request):
    """
    Subpage to details_page
    :param request: url request to get details_page
    :return: rendering the subpage based on detailed.html
    """

    return render(request, 'detailed.html')
