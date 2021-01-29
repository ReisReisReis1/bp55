"""
Possibility to add sth to Admin Interface out of this APP: details_page
"""

from django.contrib import admin

# pylint: disable = import-error, relative-beyond-top-level
from .models import Era, Building, Picture, Blueprint

admin.site.register(Era)
admin.site.register(Building)
admin.site.register(Picture)
admin.site.register(Blueprint)
