"""
URL Settings for the APP: impressum
path('',views.impressum, name='impressum'),
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, mo-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'impressum'
urlpatterns = [
    path('', views.impressum, name='impressum')
]