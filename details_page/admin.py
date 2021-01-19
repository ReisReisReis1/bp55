"""
Possibility to add sth to Admin Interface out of this APP: details_page
"""

from django.contrib import admin

# Register your models here.
# pylint: disable = import-error, relative-beyond-top-level
from .models import Era, Building, Picture

admin.site.register(Era)
admin.site.register(Building)
admin.site.register(Picture)
