"""
URL Settings for the APP: details_page
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'details_page'
urlpatterns = [
    path('detailed/<int: id>/', views.detailed),
    """path('', views.detailed, name='detailed'),"""
]
