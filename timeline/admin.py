"""
Possibility to add sth to Admin Interface out of this APP: timeline
"""
from django.contrib import admin

# Register your models here.
# pylint: disable = import-error, relative-beyond-top-level
from .models import HistoricDate

admin.site.register(HistoricDate)