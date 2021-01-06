"""

"""

from django.urls import path
# pylint: disable = import-error
from . import views

app_name = 'start'
urlpatterns = [
    path('', views.start, name='start')
]
