"""
Configurations of the Website subpages from the App: video-content
"""

from django.shortcuts import render
# pylint: disable = import-error,relative-beyond-top-level
from details_page.models import Era
from .models import Video
from impressum.views import get_course_link


def display(request):
    """
    Subpage to show all videos sorted into fitting era
    :param request: url request to get subpage /videos
    :return: rendering the subpage based on videos.html
    with a context variable to get Videos sorted in eras
    """
    # pylint: disable = no-member
    eras = Era.objects.filter(visible_on_video_page=True).exclude(year_from=None)
    eras = sorted(eras, key=lambda er_a: er_a.get_year_of_item_as_signed_int())
    eras_context = {}
    # Add all eras that do not have an year_from
    # pylint: disable = no-member
    eras = eras + list(Era.objects.filter(year_from=None, visible_on_video_page=True))
    for era in eras:
        eras_context[era] = Video.get_era(Video, era.name)

    context = {
        'Era': eras_context,
        'Kurs_Link': get_course_link()
    }
    return render(request, 'videos.html', context)
