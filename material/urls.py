"""
URL Settings for the APP: material
"""

from django.urls import include, path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'material'
urlpatterns = [
    path('', views.material, name='material'),
    ]
