"""

"""

from django.shortcuts import render
# pylint: disable = import-error, no-name-in-module
from video_content.models import Videos


# Create your views here.


def start(request):
    """
    Subpage start
    :param request: url request to subpage /start
    :return: rendering the subpage based on start.html
    """
    # pylint: disable = no-member
    video = Videos.objects.get(title='VL_Archaik-1-3')
    context = {
        'video': video
    }
    return render(request, 'start.html', context)
