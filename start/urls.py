"""
URL Settings for the APP: start
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'start'
urlpatterns = [
    path('', views.start, name='start')
]
