"""
Configurations of the different functions and subpages from the App: search
"""
from django.db.models import Q
from django.shortcuts import render
# pylint: disable = no-name-in-module, import-error
from details_page.models import Building
from timeline.views import get_thumbnails_for_buildings
from impressum.views import get_course_link


def search(request):
    """
    Function to search in buildings
    :param request: url request to make a search with the search criteria
    :return: rendering the subpage based on search.html with context
    context: Variable to search all buildings with the criteria got from the request
    """
    search_request = request.GET.get('search_request', '')
    results = Building.objects.filter(Q(name__icontains=search_request) |
                                      Q(city__icontains=search_request) | \
                                      Q(region__icontains=search_request) | \
                                      Q(country__icontains=search_request) | \
                                      Q(era__name__icontains=search_request) | \
                                      Q(architect__icontains=search_request) | \
                                      Q(context__icontains=search_request) | \
                                      Q(builder__icontains=search_request) | \
                                      Q(construction_type__icontains=search_request) | \
                                      Q(design__icontains=search_request) | \
                                      Q(function__icontains=search_request) | \
                                      Q(column_order__icontains=search_request) | \
                                      Q(material__icontains=search_request) | \
                                      Q(construction__icontains=search_request))
    # order results alphabetically:
    results = results.order_by("name")
    # adding thumbnails:
    results = get_thumbnails_for_buildings(results)
    context = {
        'Result': results,
        'Active_Filter': request.GET,
        'Kurs_Link': get_course_link()
    }
    return render(request, 'search.html', context)
