"""

"""

from django.urls import path
# pylint: disable = import-error
from . import views

app_name = 'filter_page'
urlpatterns = [
    path('', views.building_filter, name='filter'),
]
