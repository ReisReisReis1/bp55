"""
Possibility to add sth to Admin Interface out of this APP: details_page
"""

from django.contrib import admin

# pylint: disable = import-error, relative-beyond-top-level
from .models import Era, Building, Picture, Blueprint


@admin.register(Era)
class EraAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'Era'
    """
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'Building'
    """
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'Picture'
    """
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Blueprint)
class BlueprintAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'Blueprint'
    """
    search_fields = ('name',)
    ordering = ('name',)
