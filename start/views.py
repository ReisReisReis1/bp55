"""

"""

from django.shortcuts import render
# pylint: disable = import-error, no-name-in-module
from video_content.models import Video


# Create your views here.


def start(request):
    """
    Subpage start
    :param request: url request to subpage /start
    :return: rendering the subpage based on start.html
    """
    # pylint: disable = no-member
    video = Video.get_intro()
    context = {
        'video': video
    }
    return render(request, 'start.html', context)
