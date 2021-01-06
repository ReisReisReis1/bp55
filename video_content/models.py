"""
Configurations for the Database-Models in video-contents
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Video(models.Model):
    """
    Set a Model for Video
    """
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    era = models.CharField(max_length=100,
                           choices=[
                               ('Frühzeit', 'Frühzeit'), ('Archaik', 'Archaik'),
                               ('Klassik', 'Klassik'), ('Hellenismus', 'Hellenismus'),
                               ('Römische Kaiserzeit', 'Römische Kaiserzeit'), ('Spätantike', 'Spätantike'),
                               ('Keine Epoche', 'Keine Epoche'),
                                    ])
    intro = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)
    # TODO improve for more then one intro-video
    def get_intro(self):
        try:
            self.objects.get(self, intro=True)
        except ObjectDoesNotExist:
            return


    def get_era(self, wanted_era):
        return self.objects.filter(era=wanted_era)

    # pylint: disable = too-few-public-methods
