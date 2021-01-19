"""
URL Settings for the APP: home
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'filter_page'
urlpatterns = [
    path('', views.display_building_filter, name='filter'),
]
