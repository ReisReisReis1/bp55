"""

"""

from django.urls import path
# pylint: disable = import-error
from . import views

app_name = 'video_content'
urlpatterns = [
    path('', views.display, name='videos'),

]
