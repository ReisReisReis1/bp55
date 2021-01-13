"""
Configurations of the different viewable functions and subpages from the App: home
"""


from django.shortcuts import render

# Create your views here.


def building_filter(request):
    """
    Subpage "Gebäudefilter"
    :param request: url request to get subpage /filter
    :return: rendering the subpage based on filter.html
    """
    return render(request, 'filter.html')
