"""
Configurations of the Website subpages from the App: materials_page
"""

from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from .models import Material


def get_categories_and_corresponding_files():
    result = dict()
    for material_entry in Material.objects.all():
        if material_entry.category not in result:
            result[material_entry.category] = [material_entry]
        else:
            result[material_entry.category] = result[material_entry.category] + [material_entry]
    return result


def material(request):
    """
    Subpage to show the characteristics of a building
    :param request: url request to get materials_page
    :return: rendering the subpage based on material.html
    with a context variable to get the characteristics
    """

    context = {
        'Materials': get_categories_and_corresponding_files(),
    }
    return render(request, "material.html", context)
