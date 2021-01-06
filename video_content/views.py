"""
Configurations of the Website subpages from the App: video-content
"""


from django.shortcuts import render, redirect
# pylint: disable = import-error
from .models import Video


def upload_video(request):
    """
    Subpage to upload videos
    :param request: url request to subpage /upload
    :return: rendering the subpage based on upload.html
    """


def display(request):
    """
    Subpage to show all videos sorted into fitting era
    :param request: url request to subpage /videos
    :return: rendering the subpage based on videos.html
    """

    context = {
        'Frühzeit': Video.get_era(Video, 'Frühzeit'),
        'Archaik': Video.get_era(Video, 'Archaik'),
        'Klassik': Video.get_era(Video, 'Klassik'),
        'Hellenismus': Video.get_era(Video, 'Hellenismus'),
        'RömischeKaiserzeit': Video.get_era(Video, 'Römische Kaiserzeit'),
        'Spätantike': Video.get_era(Video, 'Spätantike'),
    }

    return render(request, 'videos.html', context)
