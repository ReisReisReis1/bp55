"""
Configurations of the different viewable functions and subpages from the App: timeline
"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from details_page.models import Building, Picture, Era, get_year_as_signed_int
from timeline.models import HistoricDate
from impressum.views import get_course_link


def sorted_eras_with_buildings(items):
    """
    Building a dictionary with all eras and sorted the historic dates and buildings into the eras
    :param items: sorted list with all buildings and historic dates
    """
    era_dict = {}

    # Sort it with years as key, ascending
    items = sorted(items, key=lambda i: get_start_year_of_item(i))

    # Getting all existing eras
    all_eras = Era.objects.all()
    # Ordering the before and after the birth and christ
    all_eras_vchr = all_eras.filter(year_from_BC_or_AD="v.Chr.").order_by('-year_from')
    all_eras_nchr = all_eras.filter(year_from_BC_or_AD="n.Chr.").order_by('year_from')
    # first making a list of dicts with name as key and the struct as value
    all_eras_vchr = [{i.name: i} for i in all_eras_vchr]
    all_eras_nchr = [{i.name: i} for i in all_eras_nchr]
    # merging the lists
    all_eras = all_eras_vchr + all_eras_nchr
    # second making the list of dictionaries to one dictionary
    for era in all_eras:
        key = list(era.keys())[0]
        value = list(era.values())
        era_dict[key] = value

    for era, era_struct in era_dict.items():
        items_era_sorted = []  # list will be filled with the items fitting into the era
        era_date_range = get_year_as_signed_int(era_struct[0])  # getting the range of the era
        for item in items:
            if isinstance(item, tuple):  # differ between buildings and historic dates
                year_of_building = get_year_as_signed_int(item[0])[0]
                # item fits into the era?
                if year_of_building in range(era_date_range[0], era_date_range[1]):
                    # Building tupel
                    items_era_sorted.append((True, item[0], get_date_as_str(item), item[1]))

            else:  # item is a historic date
                year_of_historic_date = item.get_year_as_signed_int()
                # item fits into the era?
                if year_of_historic_date in range(era_date_range[0], era_date_range[1]):
                    items_era_sorted.append((False, item, get_date_as_str(item), None))

        era_dict[era] = (era_struct[0], items_era_sorted)
    return era_dict


def get_thumbnails_for_buildings(building_list):
    """
    This method will provide functionality for finding thumbnails for buildings.
    For every thumbnail in the list buildings_list (can also be a QuerySet),
    it will search the Pictures objects, and return the thumbnail.
    If there is more than one possible thumbnail it will choose one randomly.
    If there is no thumbnail for a building, it will set and return None for it.
    :param building_list: A list of buildings you want to get thumbnails for.
    :return: Will return an tuple: The building from building_list, along with the thumbnail or
    default thumbnail. Or empty list, if building was empty.
    """
    # pylint: disable = no-member
    buildings_with_thumbnails = []
    # Search for thumbnails
    for building in building_list:
        try:
            buildings_with_thumbnails.append((building,
                                              Picture.objects.get(building=building.pk,
                                                                  usable_as_thumbnail=True)))
        except Picture.DoesNotExist:
            buildings_with_thumbnails.append((building, None))
        except Picture.MultipleObjectsReturned:
            possible_thumbnails = Picture.objects.filter(building=building.pk,
                                                         usable_as_thumbnail=True)
            buildings_with_thumbnails.append((building, possible_thumbnails[0]))
    return buildings_with_thumbnails


def get_start_year_of_item(i):
    """
    Method used the call of helpers for the two different classes
    :param i: the item to call the helper for
    :return: the year of an Historic Date, or the date_from of an Building, as Signed int,
    as calculated by the called helper.
    """
    # A Building is a tuple with its thumbnail, [0] to get Building
    result = None
    if isinstance(i, tuple):
        result = get_year_as_signed_int(i[0])[0]
    elif isinstance(i, HistoricDate):
        result = i.get_year_as_signed_int()
    return result


def get_date_as_str(item):
    """
    Method to get the Date as String (for the frontend)
    This will also mange getting the exacter Date or just the number of the year
    for historic dates.
    :param item: the item to get the date for
    :return: an String with the date
                (buildings: year number for beginning of the construction,
                historic dates: exact date (if present), otherwise year number.
                Each along with BC/AD).
    """
    result = None
    if isinstance(item, tuple):
        # Building is a tuple with its thumbnail, therefore [0] to get the building
        year_from = str(item[0].year_from) if item[0].year_from is not None else '9999'
        century = '. Jh. ' if item[0].year_century else ' '
        ca = 'ca. ' if item[0].year_ca else ''
        result = ca + year_from + century + str(item[0].year_from_BC_or_AD)
    elif isinstance(item, HistoricDate):
        if item.exacter_date is None:
            century = '. Jh. ' if item.year_century else ' '
            ca = 'ca. ' if item.year_ca else ''
            result = ca + str(item.year) + century + str(item.year_BC_or_AD)
        else:
            result = str(item.exacter_date.day) + '.' + str(item.exacter_date.month) + '.' + str(
                item.exacter_date.year) + " " + str(item.year_BC_or_AD)
    return result


def timeline(request):
    """
    Subpage "Zeitachse"
    :param request: url request to get subpage /timeline
    :return: rendering the subpage based on timeline.html
    """
    # get only buildings with dates set
    # pylint: disable = no-member
    buildings = Building.objects.all()
    buildings = get_thumbnails_for_buildings(buildings)
    # get historic dates (they must have a date (not nullable database field))
    historic_dates = HistoricDate.objects.all()
    # Make lists from QuerySets
    # because otherwise pythons list concatenation and sorting will not work
    items = list(buildings) + list(historic_dates)

    context = {
        'Eras_Buildings': sorted_eras_with_buildings(items),
        'Kurs_Link': get_course_link(),
    }

    return render(request, 'timeline.html', context)
