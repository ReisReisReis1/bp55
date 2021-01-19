"""
Configurations of the different functions and subpages from the App: search
"""
from django.db.models import Q
from django.shortcuts import render
from details_page.models import Building


def search(request):
    """
    Function to search in buildings
    :param request: url request to make a search
    :return: if the request.method is a post,
             then return the rendered search.html with the search results
             else return nothing
    """
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        results = Building.objects.filter(Building, Q(name__icontains=search_id) |
                                          Q(city__icontains=search_id) | \
                                          Q(region__icontains=search_id) | \
                                          Q(country__icontains=search_id) | \
                                          Q(era__name__icontains=search_id) | \
                                          Q(architect__icontains=search_id) | \
                                          Q(context__iscontains=search_id) | \
                                          Q(builder__iscontains=search_id) | \
                                          Q(construction_type=search_id) | \
                                          Q(design__icontains=search_id) | \
                                          Q(function__icontains=search_id) | \
                                          Q(column_order__iscontains=search_id))
        context = {
            'Result': results
        }
        return render(request, 'search.html', context)
