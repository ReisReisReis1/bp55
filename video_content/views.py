"""
Configurations of the Website subpages from the App: video-content
"""


from django.shortcuts import render
# pylint: disable = import-error,relative-beyond-top-level
from .models import Video


def display(request):
    """
    Subpage to show all videos sorted into fitting era
    :param request: url request to get subpage /videos
    :return: rendering the subpage based on videos.html
    with a context variable to get Videos sorted in eras
    """

    context = {
        'Frühzeit': Video.get_era(Video, 'Frühzeit'),
        'Archaik': Video.get_era(Video, 'Archaik'),
        'Klassik': Video.get_era(Video, 'Klassik'),
        'Hellenismus': Video.get_era(Video, 'Hellenismus'),
        'RömischeKaiserzeit': Video.get_era(Video, 'Römische Kaiserzeit'),
        'Spätantike': Video.get_era(Video, 'Spätantike'),

        'Era': (Video.get_era(Video, 'Frühzeit'),
                Video.get_era(Video, 'Archaik'),
                Video.get_era(Video, 'Klassik'),
                Video.get_era(Video, 'Hellenismus'),
                Video.get_era(Video, 'Römische Kaiserzeit'),
                Video.get_era(Video, 'Spätantike')),
    }

    return render(request, 'videos.html', context)
