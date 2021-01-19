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
    return Building.objects.filter(Q(city__icontains=criteria[0]) |
                                   Q(region__icontains=criteria[1]) |
                                   Q(country__icontains=criteria[2]) |
                                   Q(era__name__icontains=criteria[3]) |
                                   Q(architect__icontains=criteria[4]) |
                                   Q(builder__icontains=criteria[5]) |
                                   Q(design__icontains=criteria[6]) |
                                   Q(column_order__icontains=criteria[7]))


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
