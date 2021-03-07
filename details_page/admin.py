"""
Possibility to add sth to Admin Interface out of this APP: details_page
"""

from django.contrib import admin

# pylint: disable = import-error, relative-beyond-top-level
from .models import Era, Building, Picture, Blueprint


class BlueprintInLine(admin.StackedInline):
    """
    Model for the possibility to create a blueprint during the creation of an building
    """
    model = Blueprint


class PictureInLine(admin.StackedInline):
    """
    Model for the possibility to create a picture during the creation of an building
    """
    model = Picture


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
    inlines = [
        BlueprintInLine,
        PictureInLine,
    ]
