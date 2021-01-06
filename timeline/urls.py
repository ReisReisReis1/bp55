"""

"""

from django.urls import path
# pylint: disable = import-error
from . import views

app_name = 'timeline'
urlpatterns = [
    path('', views.timeline, name='timeline'),
]
