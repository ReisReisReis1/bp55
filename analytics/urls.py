from django.urls import path
from .views import analytics_view, add_visit, delete_old, line_chart, line_chart_json

app_name = "analytics"
urlpatterns = [
    path('', analytics_view, name='analytics'),
    path('add/<str:page>/<int:object_id>/', add_visit, name='add_visit'),
    path('delete/', delete_old, name="delete_old"),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]