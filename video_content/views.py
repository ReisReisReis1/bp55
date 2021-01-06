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
    if request.method == 'POST':
        title = request.POST['title']
        video = request.POST['video']

        content = Video(title=title, video=video)
        content.save()
        return redirect('home')

    return render(request, 'upload.html')


def display(request):
    """
    Subpage to show all videos
    :param request: url request to subpage /videos
    :return: rendering the subpage based on videos.html
    """
    videos = Video.objects.all()
    context = {
        'videos': videos,
    }

    return render(request, 'videos.html', context)
