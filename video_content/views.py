"""
Configurations of the Website subpages from the App: video-content
"""

from django.shortcuts import render
# pylint: disable = import-error,relative-beyond-top-level, no-name-in-module
from details_page.models import Era
from start.views import login_required
from impressum.views import get_course_link
from announcements.views import get_announcements
from analytics.views import register_visit
from .models import Video


# Hier einkommentieren für SSO:
#@login_required
def display(request):
    """
    Subpage to show all videos sorted into fitting era
    :param request: url request to get subpage /videos
    :return: rendering the subpage based on videos.html
    with a context variable to get Videos sorted in eras
    """
    register_visit(request, "Videoseite")
    # pylint: disable = no-member
    eras = Era.objects.filter(visible_on_video_page=True).exclude(year_from=None)
    eras = sorted(eras, key=lambda er_a: er_a.get_year_as_signed_int()[0])
    eras_context = []
    # Add all eras that do not have an year_from
    # pylint: disable = no-member
    eras = eras + list(Era.objects.filter(year_from=None, visible_on_video_page=True))
    i = 0
    for i in range(len(eras)):
        # Era on the last position has no next color
        nextcolor = None
        if i != len(eras)-1:
            nextcolor = eras[i+1].color_code
        videos = Video.get_era(Video, eras[i].name)
        # alphanumeric sort of videos
        videos = sorted(videos, key=lambda v: v.title)
        eras_context.append((eras[i], videos, nextcolor))

    context = {
        'Era': eras_context,
        'Kurs_Link': get_course_link(),
        'announcements': get_announcements(),
    }
    return render(request, 'videos.html', context)
