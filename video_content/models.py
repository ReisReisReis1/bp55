"""
Configurations for the Database-Models in video-contents
"""
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.db.models import Q
from details_page.models import Era


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
    era = models.ForeignKey(to=Era, on_delete=models.SET_NULL, null=True, help_text="Epoche des Videos auswählen.",
                            related_name="+")
    era2 = models.ForeignKey(to=Era, on_delete=models.SET_NULL, blank=True, null=True,
                             help_text="""Falls das Video in zwei Epochen fällt, kann hier eine zweite
                             hinzugefügt werden. Diese Feld kann auch leer bleiben.""", related_name="+")
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
        except ObjectDoesNotExist:
            return ObjectDoesNotExist
        except MultipleObjectsReturned:
            # pylint: disable= no-member
            return self.objects.filter(intro=True).first
        return intro

    def get_era(self, wanted_era):
        """
        Getting a List of Videos with the given era
        :param wanted_era: Era id (pk),
        :return: List of videos with given era or empty list
        """
        # pylint: disable= no-member
        # imported and added models.Q, to realise and OR lookup (so either on is the searched era)
        videos = self.objects.filter(Q(era=wanted_era) | Q(era2=wanted_era))
        return videos

    # pylint: disable = too-few-public-methods
