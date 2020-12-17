from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('zeitstrahl', views.zeitstrahl, name='zeitstrahl'),
    path('themengrid', views.themengrid, name='themengrid'),
    path('t', views.t , name='t'),
    path('header', views.header, name='header'),
]
