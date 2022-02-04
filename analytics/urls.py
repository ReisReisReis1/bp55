from django.urls import path
from .views import analytics_view, add_visit, delete_old

app_name = "analytics"
urlpatterns = [
    path('', analytics_view, name='analytics'),
    path('add/<str:page>/<int:object_id>/', add_visit, name='add_visit'),
    path('delete/', delete_old, name="delete_old")
]