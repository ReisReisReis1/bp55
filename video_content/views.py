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

    eras = Era.objects.filter(visible_on_video_page=True).exclude(year_from=None)
    eras = sorted(eras, key=lambda era: era.get_year_of_item_as_signed_int(era))
    eras_context = {}
    # Add all eras that do not have an year_from
    eras = eras + list(Era.objects.filter(year_from=None, visible_on_video_page=True))
    for e in eras:
        eras_context[e] = Video.get_era(Video, e.name)
    context = {
        'Era': eras_context,
    }
    return render(request, 'videos.html', context)

