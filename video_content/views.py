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

    def get_year_of_item_as_signed_int(era):
        """
        Inner helper to sorting the years.
        About the try/except: You can define an Era without an year. This leads to following problem:
        You can not sort Eras by year if there is one without an year. In line 29 or 31 we try to get the
        year as an Int. This will raise the TypeError, if this Era don't has a year (or the year is set
        to None to be exact). Therefore we except this error, and return 2021, which is higher than
        every year in the Database (limited to max_years (currently 1400)).
        :param era: the era to get the year from
        :return: the year of the era(beginning year)
        """
        try:
            if era.year_from_BC_or_AD == "v.Chr.":
                return -1 * int(era.year_from)
            else:
                return int(era.year_from)
        except TypeError:
            # If era has no year return 2021, so it will be listed last.
            return 9999999999999999999

    eras = Era.objects.filter(visible_on_video_page=True).exclude(year_from=None)
    eras = sorted(eras, key=lambda era: get_year_of_item_as_signed_int(era))
    eras_context = {}
    # Add all eras that do not have an year_from
    eras = eras + list(Era.objects.filter(year_from=None))
    for e in eras:
        eras_context[e.name] = Video.get_era(Video, e.name)
    context = {
        'Era': eras_context,
    }
    return render(request, 'videos.html', context)

