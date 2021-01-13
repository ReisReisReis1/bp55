"""
URL Settings for the APP: video_content
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'video_content'
urlpatterns = [
    path('', views.display, name='videos'),

]
