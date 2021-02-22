"""
Configurations of the Website subpages from the App: materials_page
"""

from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level


def impressum(request):

    return render(request, "impressum.html")
