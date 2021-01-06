"""
Configurations for the Database-Models in video-contents
"""


from django.db import models


class Videos(models.Model):
    """
    Set a Model for Videos
    """
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    era = models.CharField(max_length=100)

    def __str__(self):
        return str(self.title)
    # TODO: public methods
    # pylint: disable = too-few-public-methods