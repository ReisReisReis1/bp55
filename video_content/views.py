"""
Configurations of the Website subpages from the App: video-content
"""


from django.shortcuts import render
# pylint: disable = import-error,relative-beyond-top-level
from .models import Video
from details_page.models import Era


def display(request):
    """
    Subpage to show all videos sorted into fitting era
    :param request: url request to get subpage /videos
    :return: rendering the subpage based on videos.html
    with a context variable to get Videos sorted in eras
    """

    eras = Era.objects.all().order_by()
    context = {}
    for e in eras:
        context[e.name] = Video.get_era(Video, e.pk)
    return render(request, 'videos.html', context)
