"""
URL Settings for the APP: imressum_page
path('', views.material, name='impressum),
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'impressum_page'
urlpatterns = [
    path('', views.impressum, name='impressum'),
]