"""
Configurations of the different viewable functions and subpages from the App: timeline
"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from details_page.models import Building, Picture, Era
from timeline.models import HistoricDate


def getting_all_eras_sorted():
    """
    Getting all eras sorted into a dictionary, also with new eras,
    that represent the overlapping eras
    """
    # Getting all existing eras
    all_eras = Era.objects.all()
    # Hardcoding the order of the eras with overlapping eras
    era_dict = {
        'Bronzezeit': (),
        'Frühe Eisenzeit': (),
        'Archaik': (),
        'Archaik_Königszeit': (),
        'Königszeit': (),
        'Königszeit_Klassik': (),
        'Klassik': (),
        'Klassik_Republik': (),
        'Republik': (),
        'Republik_Hellenismus': (),
        'Hellenismus': (),
        'Frühe Kaiserzeit': (),
        'Mittlere Kaiserzeit': (),
        'Späte Kaiserzeit': (),
        'Spätantike': (),
    }
    # adding the structs to the eras
    # the first part of the tupel is the era-struct , the second is a possible second er-struct
    # and the third is a boolean, if the era should be seen in the legend or not
    for era in era_dict:
        era_list = list(all_eras.filter(name=era))
        if era_list:
            era_dict[era] = (era_list[0], None, True)
        else:
            era_dict[era] = (None, None, True)
    # the edge cases for the overlapping eras
    era_dict['Archaik_Königszeit'] = (era_dict['Archaik'][0], era_dict['Königszeit'][0], False)
    era_dict['Königszeit_Klassik'] = (era_dict['Königszeit'][0], era_dict['Klassik'][0], False)
    era_dict['Klassik_Republik'] = (era_dict['Klassik'][0], era_dict['Republik'][0], False)
    era_dict['Republik_Hellenismus'] = (era_dict['Republik'][0], era_dict['Hellenismus'][0], False)

    return era_dict


def sort_into_eras(items):
    """
    Sorting the buildings and historic dates into the suited era using the dates
    """
    sorted_eras = {
        'Bronzezeit': [],  # 1400 - 1100 v.Chr.
        'Frühe Eisenzeit': [],  # 1100 - 700 v.Chr.
        'Archaik': [],  # 700 - 620 v.Chr.
        'Archaik_Königszeit': [],  # 620 - 509 v.Chr.
        'Königszeit_Klassik': [],  # 509 - 500 v.Chr.
        'Klassik_Republik': [],  # 500 - 336 v.Chr.
        'Republik_Hellenismus': [],  # 336 - 31 v.Chr.
        'Frühe Kaiserzeit': [],  # 31 v.Chr. - 68 n.Chr.
        'Mittlere Kaiserzeit': [],  # 68 - 192 n.Chr.
        'Späte Kaiserzeit': [],  # 192 - 284 n.Chr.
        'Spätantike': [],  # 284 - 565 n.Chr.
    }

    for item in items:
        date = get_year_of_item(item)
        if date in range(-1400, -1100):
            sorted_eras['Bronzezeit'].append(item)
        if date in range(-1100, -700):
            sorted_eras['Frühe Eisenzeit'].append(item)
        if date in range(-700, -620):
            sorted_eras['Archaik'].append(item)
        if date in range(-620, -509):
            sorted_eras['Archaik_Königszeit'].append(item)
        if date in range(-509, -500):
            sorted_eras['Königszeit_Klassik'].append(item)
        if date in range(-500, -336):
            sorted_eras['Klassik_Republik'].append(item)
        if date in range(-336, -31):
            sorted_eras['Republik_Hellenismus'].append(item)
        if date in range(-31, 68):
            sorted_eras['Frühe Kaiserzeit'].append(item)
        if date in range(68, 192):
            sorted_eras['Mittlere Kaiserzeit'].append(item)
        if date in range(192, 284):
            sorted_eras['Späte Kaiserzeit'].append(item)
        if date in range(284, 565):
            sorted_eras['Spätantike'].append(item)

    return sorted_eras


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
        except ObjectDoesNotExist:
            buildings_with_thumbnails.append((building, None))
        except MultipleObjectsReturned:
            possible_thumbnails = Picture.objects.filter(building=building.pk,
                                                         usable_as_thumbnail=True)
            # set a random thumbnail out of all possible ones
            buildings_with_thumbnails.append((building, possible_thumbnails[0]))
    return buildings_with_thumbnails


# Inner helper method for items
def get_year_of_item(i):
    """
    Inner function used the call of helpers for the two different classes
    :param i: the item to call the helper for
    :return: the year of an Historic Date, or the date_from of an Building, as Signed int,
    as calculated by the called helper.
    """
    # A Building is a tuple with its thumbnail, [0] to get Building
    result = None
    if isinstance(i, tuple):
        if i[0].date_from_BC_or_AD == "v.Chr.":
            result = -1 * int(i[0].date_from)
        else:
            result = int(i[0].date_from)
    elif isinstance(i, HistoricDate):
        if i.exacter_date is None:
            if i.year_BC_or_AD == "v.Chr.":
                result = -1 * int(i.year)
            else:
                result = int(i.year)
        else:
            if i.year_BC_or_AD == "v.Chr.":
                result = -1 * int(i.exacter_date.year)
            else:
                result = int(i.exacter_date.year)
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
        result = str(item[0].date_from) + " " + str(item[0].date_from_BC_or_AD)
    elif isinstance(item, HistoricDate):
        if item.exacter_date is None:
            result = str(item.year) + " " + str(item.year_BC_or_AD)
        else:
            result = str(item.exacter_date) + " " + str(item.year_BC_or_AD)
    return result


def timeline(request):
    """
    Subpage "Zeitachse"
    :param request: url request to get subpage /timeline
    :return: rendering the subpage based on timeline.html
    """
    era_dict = getting_all_eras_sorted()

    # get only buildings with dates set
    # pylint: disable = no-member
    buildings = Building.objects.exclude(date_from=None)
    buildings = get_thumbnails_for_buildings(buildings)
    # get historic dates (they must have a date (not nullable database field))
    historic_dates = HistoricDate.objects.all()
    # Make lists from QuerySets
    # because otherwise pythons list concatenation and sorting will not work
    items = list(buildings) + list(historic_dates)
    # Sort it with years as key, ascending
    items = sorted(items, key=lambda i: get_year_of_item(i))

    sorted_buildings_into_eras = sort_into_eras(items)

    for era in sorted_buildings_into_eras:
        new_list = []
        for item in sorted_buildings_into_eras[era]:
            if isinstance(item, tuple):
                new_list.append((True, item[0], get_date_as_str(item), item[1]))
            else:
                new_list.append((False, item, get_date_as_str(item), None))
        sorted_buildings_into_eras[era] = new_list

    context = {
        'items': sorted_buildings_into_eras,
        'eras': era_dict,
    }

    return render(request, 'timeline.html', context)
