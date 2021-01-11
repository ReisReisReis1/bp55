"""
URL Settings for the APP: timeline
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'timeline'
urlpatterns = [
    path('', views.timeline, name='timeline'),
]
