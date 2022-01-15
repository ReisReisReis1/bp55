from django.urls import include, path
from .views import analytics_view

app_name = "analytics"
urlpatterns = [
    path('', analytics_view, name='analytics')
]