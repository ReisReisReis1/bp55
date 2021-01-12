"""
Possibility to add sth. to Admin Interface out of this APP: video_content
"""
from django.contrib import admin

# Register your models here.
# pylint: disable = import-error, relative-beyond-top-level
from .models import Video

admin.site.register(Video)
