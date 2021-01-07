"""
Configurations for the Database-Models in video-contents
"""
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models


class Video(models.Model):
    """
    Set a model for video
    titel: Name of the video
    video: Path to the video-file
    era: The Era that the video is about
    intro: Checkbox, if it's the entry video or not
    """
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    era = models.CharField(max_length=100,
                           choices=[
                               ('Frühzeit', 'Frühzeit'), ('Archaik', 'Archaik'),
                               ('Klassik', 'Klassik'), ('Hellenismus', 'Hellenismus'),
                               ('Römische Kaiserzeit', 'Römische Kaiserzeit'), ('Spätantike', 'Spätantike'),
                               ('Sonstiges', 'Sonstiges'),
                                    ], default='Sonstiges')

    intro = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    #TODO: Lowest ID
    def get_intro(self):
        try:
            intro = self.objects.get(intro=True)
        except ObjectDoesNotExist:
            return ObjectDoesNotExist
        except MultipleObjectsReturned:
            return self.objects.filter(intro=True).get(id=1)
        return intro

    def get_era(self, wanted_era):
        try:
            videos = self.objects.filter(era=wanted_era)
        except ObjectDoesNotExist:
            return ObjectDoesNotExist
        return videos

    # pylint: disable = too-few-public-methods
