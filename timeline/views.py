"""

"""


from django.shortcuts import render

# Create your views here.


def timeline(request):
    """
    Subpage "Zeitstrahl"
    :param request: url request to subpage /timeline
    :return: rendering the subpage based on timeline.html
    """
    return render(request, 'timeline.html')
