"""
Configurations of the different viewable functions and subpages from the App: timeline
"""
# pylint: disable = no-name-in-module, import-error
from django.shortcuts import render
from details_page.models import Building, Era
from start.views import login_required
from timeline.models import HistoricDate
from impressum.views import get_course_link
from announcements.views import get_announcements


def sorted_eras_with_buildings(items):
    """
    Building a dictionary with all eras and sorted the historic dates and buildings into the eras
    :param items: sorted list with all buildings and historic dates
    """
    era_dict = {}

    # Sort it with years as key, ascending
    items = sorted(items, key=lambda i: i.get_year_as_signed_int()[0])
    # Getting all existing eras
    all_eras = Era.objects.all()
    # Ordering the before and after the birth and christ
    all_eras_vchr_db = all_eras.filter(year_from_BC_or_AD="v.Chr.").order_by('-year_from')
    all_eras_nchr = all_eras.filter(year_from_BC_or_AD="n.Chr.").order_by('year_from')
    # first making a list of dicts with name as key and the struct as value
    all_eras_vchr = []
    # This era name will be combined with "Hellenismus", and filtered out as era by it self for the
    # timeline.
    rome_overlap_name = "römische Republik"
    for era in all_eras_vchr_db:
        if era.name == "Hellenismus":
            all_eras_vchr.append({era.name+" / "+rome_overlap_name: era})
        elif era.name == rome_overlap_name:
            continue
        else:
            all_eras_vchr.append({era.name: era})
    all_eras_nchr = [{i.name: i} for i in all_eras_nchr]
    # merging the lists
    all_eras = all_eras_vchr + all_eras_nchr
    # second making the list of dictionaries to one dictionary
    for era in all_eras:
        key = list(era.keys())[0]
        value = list(era.values())[0]
        era_dict[key] = value

    i = 0
    for era, era_struct in era_dict.items():
        items_era_sorted = []  # list will be filled with the items fitting into the era
        era_date_range = era_struct.get_year_as_signed_int()  # getting the range of the era
        for item in items:
            year_of_item = item.get_year_as_signed_int()[0]
            # item fits into the era?
            if year_of_item in range(era_date_range[0], era_date_range[1]):
                # Building tupel
                if isinstance(item, Building):
                    items_era_sorted.append(
                        (True, item, item.get_thumbnail(),
                         item.get_year_and_bc_ad_as_str()[0], item.get_year_and_bc_ad_as_str()[1]))
                else:
                    items_era_sorted.append((False, item, item.get_year_as_str(), None, None))
        nextcolor = "None"
        if i != len(era_dict)-1:
            nextcolor = list(era_dict.values())[i+1].color_code

        era_dict[era] = (era_struct, items_era_sorted, nextcolor)
        i += 1

    return era_dict


# Hier einkommentieren für SSO:
#@login_required
def timeline(request):
    """
    Subpage "Zeitachse"
    :param request: url request to get subpage /timeline
    :return: rendering the subpage based on timeline.html
    """
    # get only buildings with dates set
    # pylint: disable = no-member
    buildings = Building.objects.all()
    # get historic dates (they must have a date (not nullable database field))
    historic_dates = HistoricDate.objects.all()
    # Make lists from QuerySets
    # because otherwise pythons list concatenation and sorting will not work
    items = list(buildings) + list(historic_dates)

    context = {
        'Eras_Buildings': sorted_eras_with_buildings(items),
        'Kurs_Link': get_course_link(),
        'announcements': get_announcements(),
    }

    return render(request, 'timeline.html', context)
