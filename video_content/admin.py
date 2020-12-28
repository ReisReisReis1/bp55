"""
Possibility to add sth. to Admin Interface
"""
from django.contrib import admin

# Register your models here.
# pylint: disable = import-error, relative-beyond-top-level
from .models import Videos

admin.site.register(Videos)
