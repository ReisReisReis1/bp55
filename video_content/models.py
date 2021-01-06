"""
Configurations for the Database-Models in video-contents
"""
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
            self.objects.get(intro=True)
        except ObjectDoesNotExist:
            return ObjectDoesNotExist
        except MultipleObjectsReturned:
            return self.objects.filter(intro=True).get(id=1)

    def get_era(self, wanted_era):
        try:
            self.objects.filter(era=wanted_era)
        except ObjectDoesNotExist:
            return ObjectDoesNotExist

    # pylint: disable = too-few-public-methods
