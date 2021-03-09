"""
possibility to add sth to Admin Interface out of this APP: impressum
"""

from django.contrib import admin

# pylint: disable = import-error, relative-beyond-top-level
from .models import Impressum

@admin.register(Impressum)
class ImpressumAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'Impressum'
    """
    search_fields = ('name',)
    ordering = ('name',)
