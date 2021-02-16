"""
Configurations of the different viewable functions and subpages from the App: material
"""

from django.shortcuts import render


def material(request):
    """
    Subpage to material
    :param request: url request to get subpage /
    :return: rendering the subpage based on material.html
    """
    return render(request, 'material.html', )

