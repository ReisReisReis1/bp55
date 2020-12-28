"""
URL Settings for the APP: home
"""

from django.urls import path
# pylint: disable = import-error
from . import views
# pylint: disable = invalid-name
app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('zeitstrahl', views.zeitstrahl, name='zeitstrahl'),
    path('themengrid', views.themengrid, name='themengrid'),
    path('header', views.start, name='header'),
]
