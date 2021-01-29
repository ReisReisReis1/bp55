"""
Configurations of the different viewable functions and subpages from the App: timeline
"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from details_page.models import Building, Picture
from timeline.models import HistoricDate


# Create your views here.


def get_thumbnails_for_buildings(building_list):
    """
    This method will provide function for finding thumbnails for buildings.
    For every thumbnail in the list buildings_list (can also be a QuerySet),
    it will search the Pictures objects, and return the thumbnail.
    If there is more than one possible thumbnail it will choose one randomly.
    If there is no thumbnail for a building, it will set and return None for it.
    :param building_list: A list of buildings you want to get thumbnails for.
    :return: Will return an tuple: The building from building_list, along with the thumbnail or
    default thumbnail. Or empty list, if building was empty.
    """
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


def timeline(request):
    """
    Subpage "Zeitachse"
    :param request: url request to get subpage /timeline
    :return: rendering the subpage based on timeline.html
    """

    # Inner helper method for items
    def get_year_of_item(i):
        """
        Inner function used the call of helpers for the two different classes
        :param i: the item to call the helper for
        :return: the year of an Historic Date, or the date_from of an Building, as Signed int,
        as calculated by the called helper.
        """
        # A Building is a tuple with its thumbnail, [0] to get Building
        if isinstance(i, tuple):
            if i[0].date_from_BC_or_AD == "v.Chr.":
                return -1 * int(i[0].date_from)
            else:
                return int(i[0].date_from)
        elif isinstance(i, HistoricDate):
            if i.exacter_date is None:
                if i.year_BC_or_AD == "v.Chr.":
                    return -1 * int(i.year)
                else:
                    return int(i.year)
            else:
                if i.year_BC_or_AD == "v.Chr.":
                    return -1 * int(i.exacter_date.year)
                else:
                    return int(i.exacter_date.year)

    # get only buildings with dates set
    buildings = Building.objects.exclude(date_from=None)
    buildings = get_thumbnails_for_buildings(buildings)
    # get historic dates (they must have a date (not nullable database field))
    historic_dates = HistoricDate.objects.all()
    # Make lists from QuerySets because otherwise pythons list concatenation and sorting will no work
    items = list(buildings) + list(historic_dates)
    # Sort it with years as key, ascending
    items = sorted(items, key=lambda i: get_year_of_item(i))
    items_with_dates = []
    for item in items:
        if isinstance(item, tuple):
            items_with_dates.append((True, item[0], get_date_as_str(item), item[1]))
        else:
            items_with_dates.append((False, item, get_date_as_str(item), None))
    context = {
        "items": items_with_dates,
    }
    return render(request, 'timeline.html', context)


def get_date_as_str(item):
    """
    Method to get the Date as String (for the frontend)
    This will also mange getting the exacter Date or just the number of the year
    for historic dates.
    :param item: the item to get the date for
    :return: an String with the date
                (buildings: year number for beginning of the construction,
                historic dates: exact date (if present), otherwise year number. Each along with BC/AD).
    """
    if isinstance(item, tuple):
        # Building is a tuple with its thumbnail, therefore [0] to get the building
        return str(item[0].date_from) + " " + str(item[0].date_from_BC_or_AD)
    elif isinstance(item, HistoricDate):
        if item.exacter_date is None:
            return str(item.year) + " " + str(item.year_BC_or_AD)
        else:
            return str(item.exacter_date) + " " + str(item.year_BC_or_AD)
