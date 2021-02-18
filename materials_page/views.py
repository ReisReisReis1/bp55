"""
Configurations of the Website subpages from the App: materials_page
"""


from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from .models import Material


def material(request):
    """
    Subpage to show the characteristics of a building
    :param request: url request to get materials_page
    :return: rendering the subpage based on material.html
    with a context variable to get the characteristics
    """
    context = {
        'Dateien_nach_Kategorie': Material.get_category(Material)
    }
    return render(request, material.html, context)
