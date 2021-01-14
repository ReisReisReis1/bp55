"""
Configurations of the different viewable functions and subpages from the App: details_page
"""

from django.shortcuts import render
# pylint: disable = import-error, relative beyond-top-level
from .models import Building


def detailed(request):
    """
    Subpage to show the characteristics of a building
    :param request: url request to get details_page
    :return: rendering the subpage based on detailed.html
    with a context variable to get the characteristics
    """
    context = {
        'Name' : Building.get_name(Building, id),
        'Ort' : Building.get_city(Building, id),
        'Region' : Building.get_region(Building, id),
        'Land' : Building.get_date(Building, id),
        'Datum_von' : Building.get_date_from(Building, id),
        'Datum_von_BC_oder_AD' : Building.get_date_from_BC_or_AD(Building, id),
        'Datum_bis' : Building.get_date_to(Building, id),
        'Datum_bis_BC_oder_AD' : Building.get_date_to_BC_or_AD(Building, id),
        'Architekt' : Building.get_architect(Building, id),
        'Kontext/Lage' : Building.get_context(Building, id),
        'Bauherr' : Building.get_builder(Building, id),
        'Bautypus' : Building.get_construction_type(Building, id),
        'Bauform' : Building.get_design(Building, id),
        'Gattung/Funktion' :  Building.get_function(Building, id),
        'Dimension' : Building.get_dimension(Building, id),
        'Länge' : Building.get_length(Building, id),
        'Breite' : Building.get_width(Building, id),
        'Höhe' : Building.get_hight(Building, id),
        'Umfang' : Building.get_circumference(Building, id),
        'Fläche' : Building.get_area(Building, id),
        'Säulenordung' : Building.get_column_order(Building, id),
        'Konstruktion' : Building.get_construction(Building, id),
        'Material' : Building.get_material(Building, id),
        'Litertur' : Building.get_literature(Building, id),
        'Videos' : Building.get_videos(Building, id),
        'Bilder' : Building.get_Bilder(Building, id),
        'Baupläne' : Building.get_building_plan(Building, id),
    }

    return render(request, 'detailed.html', context)
