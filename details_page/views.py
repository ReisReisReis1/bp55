"""
Configurations of the different viewable functions and subpages from the App: details_page
"""

from django.shortcuts import render
# pylint: disable = import-error, relative beyond-top-level
from .models import Detail


def detailed(request):
    """
    Subpage to show the characteristics of a building
    :param request: url request to get details_page
    :return: rendering the subpage based on detailed.html
    with a context variable to get the characteristics
    """
    context = {
        'Name' : Detail.get_name(Detail),
        'Ort/Region' : Detail.get_city_region(Detail),
        'Land' : Detail.get_date(Detail),
        'Architekt' : Detail.get_architect(Detail),
        'Kontext/Lage' : Detail.get_context(Detail),
        'Bauherr' : Detail.get_builder(Detail),
        'Bautypus' : Detail.get_construction_type(Detail),
        'Bauform' : Detail.get_design(Detail),
        'Gattung/Funktion' :  Detail.get_function(Detail),
        'Dimension' : Detail.get_dimension(Detail),
        'Säulenordung' : Detail.get_column_order(Detail),
        'Konstruktion' : Detail.get_construction(Detail),
        'Material' : Detail.get_material(Detail),
        'Litertur' : Detail.get_literature(Detail),
        'Videos' : Detail.get_videos(Detail),
        'Bilder' : Detail.get_pictures(Detail),
        'Baupläne' : Detail.get_building_plan(Detail),
    }

    return render(request, 'detailed.html', context)
