"""

"""

from django.urls import path
# pylint: disable = import-error
from . import views

app_name = 'details_page'
urlpatterns = [
    path('', views.detailed, name='detailed'),
]
