"""

"""


from django.shortcuts import render

# Create your views here.


def building_filter(request):
    """
    Subpage "Gebäudefilter"
    :param request: url request to subpage /filter
    :return: rendering the subpage based on filter.html
    """
    return render(request, 'filter.html')
