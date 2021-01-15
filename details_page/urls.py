"""
URL Settings for the APP: details_page
path('', views.detailed, name='detailed'),
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'details_page'
urlpatterns = [
    path('<int:id>/detailed', views.detailed, name='detailed'),
]
