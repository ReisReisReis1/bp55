"""
Possibility to add sth. to Admin Interface out of this APP: video_content
"""
from django.contrib import admin

# Register your models here.
# pylint: disable = import-error, relative-beyond-top-level
from .models import Video, Timestamp


class TimestampInLine(admin.StackedInline):
    """
    Model for the possibility to create a timestamp during the creation of an video
    """
    model = Timestamp


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Configure the admin model for 'Video'
    """
    search_fields = ('title',)
    ordering = ('title',)
    inlines = [
        TimestampInLine,
    ]
