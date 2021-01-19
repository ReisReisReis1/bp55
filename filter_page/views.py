"""
Configurations of the different viewable functions and subpages from the App: home
"""
from django.db.models import Q
from django.shortcuts import render
from details_page.models import Building


def building_filter(criteria):
    """
    Function to filter all buildings with the given criteria
    :param criteria: the criteria the buildings will be filtered
    :return: a list with the filtered buildings
    """
    return Building.objects.filter(Q(city=criteria[0]) |
                                   Q(region=criteria[1]) |
                                   Q(country=criteria[2]) |
                                   Q(era=criteria[3]) |
                                   Q(architect=criteria[4]) |
                                   Q(builder=criteria[5]) |
                                   Q(design=criteria[6]) |
                                   Q(column_order=criteria[7]))


def display_building_filter(request):
    """
    Subpage "Gebäudefilter" with context
    :param request: url request to get subpage /filter
    :return: rendering the subpage based on filter.html with context
    context: Variable to filter all buildings with the criteria got from the request
    """
    context = {
        'Result': building_filter(request.GET.get('criteria'))
    }

    return render(request, 'filter.html', context)
