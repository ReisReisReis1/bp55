"""
Configurations of the different viewable functions and subpages from the App: details_page
"""

from django.shortcuts import render
#pylint: disable = import-error, relative beyond-top-level
from .models import Picture
# pylint: disable = import-error, relative beyond-top-level
from .models import Building
# pylint: disable = import-error, relative beyond-top-level
from .models import Blueprint
# pylint: disable = import-error, relative beyond-top-level
from video_content.models import Timestamp


def detailed(request, building_id):
    """
    Subpage to show the characteristics of a building
    :param request: url request to get details_page
    :return: rendering the subpage based on detailed.html
    with a context variable to get the characteristics
    """
    context = {
        'Name': Building.get_name(Building, building_id),
        'Era': Building.get_era(Building,building_id),
        'Beschreibung': Building.get_description(Building, building_id),
        'Ort': Building.get_city(Building, building_id),
        'Region': Building.get_region(Building, building_id),
        'Land': Building.get_country(Building, building_id),
        'Datum_von': Building.get_date_from(Building, building_id),
        'Datum_von_BC_oder_AD': Building.get_date_from_bc_or_ad(Building, building_id),
        'Datum_bis': Building.get_date_to(Building, building_id),
        'Datum_bis_BC_oder_AD': Building.get_date_to_bc_or_ad(Building, building_id),
        'Architekt': Building.get_architect(Building, building_id),
        'Kontext_Lage': Building.get_context(Building, building_id),
        'Bauherr': Building.get_builder(Building, building_id),
        'Bautypus': Building.get_construction_type(Building, building_id),
        'Bauform': Building.get_design(Building, building_id),
        'Gattung_Funktion':  Building.get_function(Building, building_id),
        
        #'Dimension': Building.get_dimension(Building, id),
        #'Videos': Building.get_videos(Building, id),
        
        'Länge': Building.get_length(Building, building_id),
        'Breite': Building.get_width(Building, building_id),
        'Höhe': Building.get_height(Building, building_id),
        'Umfang': Building.get_circumference(Building, building_id),
        'Fläche': Building.get_area(Building, building_id),
        'Säulenordung': Building.get_column_order(Building, building_id),
        'Konstruktion': Building.get_construction(Building, building_id),
        'Material': Building.get_material(Building, building_id),
        'Litertur': Building.get_literature(Building, building_id),
        'Bilder': Picture.get_picture_for_building(Picture, building_id),
        'Baupläne': Blueprint.get_blueprint_for_building(Blueprint, building_id),
        'Videos': Timestamps.get_timestamps_by_building(Timestamps, building_id),
    }

    return render(request, 'detailed.html', context)
