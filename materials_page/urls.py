"""
URL Settings for the APP: materials_page
path('', views.material, name='material),
"""

from django.urls import path
# pylint: disable = import-error, relative-beyond-top-level, no-name-in-module
from . import views

# pylint: disable = invalid-name
app_name = 'materials_page'
urlpatterns = [
    path('', views.material, name='material'),
    path('download', views.get_categories_and_corresponding_zip_files, name='download'),
]
