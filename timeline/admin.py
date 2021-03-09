"""
Possibility to add sth to Admin Interface out of this APP: timeline
"""
from django.contrib import admin

# pylint: disable = import-error, relative-beyond-top-level
from .models import HistoricDate


@admin.register(HistoricDate)
class HistoricDatesAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'HistoricDates'
    """
    search_fields = ('title',)
    ordering = ('title',)
    list_display = ('title', 'exacter_date', 'year', 'year_BC_or_AD')
