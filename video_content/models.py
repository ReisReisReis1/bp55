"""
Configurations for the Database-Models in video-contents
"""
from django.core.exceptions import MultipleObjectsReturned
from django.db import models


class Video(models.Model):
    """
    Set a model for video
    title: Name of the video
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
                               ('Römische Kaiserzeit', 'Römische Kaiserzeit'),
                               ('Spätantike', 'Spätantike'),
                               ('Sonstiges', 'Sonstiges'),
                                    ], default='Sonstiges')

    intro = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def get_intro(self):
        """
        Getting the video, where intro=true.
        If there are more then one, return ObjectDoesNotExist
        If there are more then one, return first in list
        :return: Video where the mark 'Intro' is set or ObjectDoesNotExist
        """
        try:
            # pylint: disable= no-member
            intro = self.objects.get(intro=True)
            return intro
        except Video.DoesNotExist:
            return Video.DoesNotExist
        except Video.MultipleObjects:
            # pylint: disable= no-member
            return self.objects.filter(intro=True).first

    def get_era(self, wanted_era):
        """
        Getting a List of Videos with the given era
        :param wanted_era: String,
        :return: List of videos with given era or empty list
        """
        # pylint: disable= no-member
        videos = self.objects.filter(era=wanted_era)
        return videos

    # pylint: disable = too-few-public-methods
