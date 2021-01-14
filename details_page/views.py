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
        'Name' : Building.get_name(Building),
        'Ort' : Building.get_city(Building),
        'Region' : Building.get_region(Building),
        'Land' : Building.get_date(Building),
        'Datum_von' : Building.get_date_from(Building),
        'Datum_von_BC_oder_AD' : Building.get_date_from_BC_or_AD(Building),
        'Datum_bis' : Building.get_date_to(Building),
        'Datum_bis_BC_oder_AD' : Building.get_date_to_BC_or_AD(Building),
        'Architekt' : Building.get_architect(Building),
        'Kontext/Lage' : Building.get_context(Building),
        'Bauherr' : Building.get_builder(Building),
        'Bautypus' : Building.get_construction_type(Building),
        'Bauform' : Building.get_design(Building),
        'Gattung/Funktion' :  Building.get_function(Building),
        'Dimension' : Building.get_dimension(Building),
        'Länge' : Building.get_length(Building),
        'Breite' : Building.get_width(Building),
        'Höhe' : Building.get_hight(Building),
        'Umfang' : Building.get_circumference(Building),
        'Fläche' : Building.get_area(Building),
        'Säulenordung' : Building.get_column_order(Building),
        'Konstruktion' : Building.get_construction(Building),
        'Material' : Building.get_material(Building),
        'Litertur' : Building.get_literature(Building),
        'Videos' : Building.get_videos(Building),
        'Bilder' : Building.get_Bilder(Building),
        'Baupläne' : Building.get_building_plan(Building),
    }

    return render(request, 'detailed.html', context)
