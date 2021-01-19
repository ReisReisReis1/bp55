"""
Configurations of the different viewable functions and subpages from the App: timeline
"""


from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from details_page.models import Building, Picture
from timeline.models import HistoricDate
import random

# Create your views here.


def timeline(request):
    """
    Subpage "Zeitachse"
    :param request: url request to get subpage /timeline
    :return: rendering the subpage based on timeline.html
    """
    # Inner helper method for items
    def getYearOfItem(item):
        """
        Inner function used the call of helpers for the two different classes
        :param item: the item to call the helper for
        :return: the year of an Historic Date, or the date_from of an Building, as Signed int,
        as calculated by the called helper.
        """
        if isinstance(item, Building):
            if item.date_from_BC_or_AD == "v.Chr.":
                return -1*int(item.date_from)
            else:
                return int(item.date_from)
        elif isinstance(item, HistoricDate):
            if item.exacter_date is None:
                if item.year_BC_or_AD == "v.Chr.":
                    return -1*int(item.year)
                else:
                    return int(item.year)
            else:
                if item.year_BC_or_AD == "v.Chr.":
                    return -1*int(item.exacter_date.year)
                else:
                    return int(item.exacter_date.year)

    # get only buildings with dates set
    buildings = Building.objects.filter(~Q(date_from=None))
    thumbnails = {}
    # Search for thumbnails
    for building in buildings:
        try:
            thumbnails[building.pk] = Picture.objects.get(building=building.pk, usable_as_thumbnail=True)
        except ObjectDoesNotExist:
            thumbnails[building.pk] = None
        except MultipleObjectsReturned:
            possible_thumbnails = Picture.objects.filter(building=building.pk, usable_as_thumbnail=True)
            # set a random thumbnail out of all possible ones
            thumbnails[building.pk] = possible_thumbnails[random.randint(0, len(possible_thumbnails)-1)]

    historic_dates = HistoricDate.objects.all()
    # Make lists from QuerySets because otherwise pythons list concatenation and sorting will no work
    items = list(buildings)+list(historic_dates)
    # Sort it with years as key, ascending
    items = sorted(items, key=lambda item: getYearOfItem(item))

    # save all in context
    context = {
        "items": items,
        "thumbnails": thumbnails,
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
    if isinstance(item, Building):
        return str(item.date_from)+" "+str(item.date_from_BC_or_AD)
    elif isinstance(item, HistoricDate):
        if item.exacter_date is None:
            return str(item.year) + " " + str(item.year_BC_or_AD)
        else:
            return str(item.exacter_date) + " " + str(item.year_BC_or_AD)



