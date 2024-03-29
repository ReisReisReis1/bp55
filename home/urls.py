"""
URL Settings for the APP: home
"""

from django.urls import include, path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('start', include('start.urls'), name='start'),

    ]
