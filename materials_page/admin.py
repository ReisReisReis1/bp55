"""
Possibility to add sth to Admin Interface out of this APP: materials_page
"""

from django.contrib import admin

# pylint: disable = import-error, relative-beyond-top-level
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'Material'
    """
    search_fields = ('name',)
    ordering = ('name',)
