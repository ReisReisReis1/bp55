"""
Configurations for the Database-Models in video-contents
"""

from django.db import models
from django.core.validators import  MaxValueValidator
from django.db.models import Q
# pylint: disable=import-error
from details_page.models import Building, Era


class Video(models.Model):
    # pylint: disable = too-few-public-methods
    """
    Set a model for video
    title: Name of the video
    video: Path to the video-file
    era: The Era that the video is about
    intro: Checkbox, if it's the entry video or not
    """

    class Meta:
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    title = models.CharField(verbose_name='Titel', max_length=100, help_text='Titel des Videos')
    video = models.FileField(verbose_name='Video', upload_to='videos/',
                             help_text='Videodatei in .mp4')
    thumbnail = models.ImageField(height_field="height", width_field="width",
                                  help_text="Hier das Vorschaubild zum Video hochladen.",
                                  upload_to="pics/thumbnails/", null=True, default=None)
    width = models.IntegerField(editable=False, default=0)
    height = models.IntegerField(editable=False, default=0)
    era = models.ForeignKey(verbose_name='1. Epoche', to=Era, on_delete=models.SET_NULL, null=True,
                            help_text="Epoche des Videos auswählen.",
                            related_name="+")
    era2 = models.ForeignKey(verbose_name='2. Epoche', to=Era, on_delete=models.SET_NULL,
                             blank=True, null=True,
                             help_text="""Falls das Video in zwei Epochen fällt,
                             kann hier eine zweite
                             hinzugefügt werden. Diese Feld kann auch leer bleiben.""",
                             related_name="+")
    intro = models.BooleanField(verbose_name='Einführung', default=False,
                                help_text='Ist dieses Video das Intro-Video?')

    def __str__(self):
        """
        Returning the title of the video as string
        """
        return str(self.title)

    def get_intro(self):
        # pylint: disable= no-member
        """
        Getting the video, where intro=true.
        If there are more then one, return ObjectDoesNotExist
        If there are more then one, return first in list
        :return: Video where the mark 'Intro' is set or ObjectDoesNotExist
        """
        try:
            intro = self.objects.get(intro=True)
            return intro
        except Video.DoesNotExist:
            return Video.DoesNotExist
        except Video.MultipleObjectsReturned:
            return self.objects.filter(intro=True)[0]

    def get_era(self, wanted_era):
        # pylint: disable= no-member
        """
        Getting a List of Videos with the given era
        :param wanted_era: Era id (pk),
        :return: QuerySet of videos with given era or empty list
        """
        # imported and added models.Q, to realise and OR lookup (so either on is the searched era)
        videos = self.objects.filter(Q(era__name=wanted_era) | Q(era2__name=wanted_era))
        return videos

    # pylint: disable = too-few-public-methods


class Timestamp(models.Model):
    """
    Model for timestamps in a video assigned to a building
    """

    class Meta:
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Timestamp'
        verbose_name_plural = 'Timestamps'

    building = models.ForeignKey(verbose_name='Gebäude', to=Building, on_delete=models.SET_NULL,
                                 null=True, help_text='Zugehöriges Gebäude')
    video = models.ForeignKey(verbose_name='Video', to=Video, on_delete=models.CASCADE, null=False,
                              help_text='Zugehöriges Video')
    minutes = models.PositiveIntegerField(verbose_name='Minuten',
                                          help_text='Geben Sie hier die Minuten an, '
                                                    'an dem das gewählte Gebäude im Video '
                                                    'erscheint'
                                                    '(Wird mit den Sekunden verbunden)')
    seconds = models.PositiveIntegerField(verbose_name='Sekunden',
                                          validators=[
                                              MaxValueValidator(59, 'Sekunden können nur zwischen '
                                                                    '0 und 60 (exklusiv) '
                                                                    'angegeben werden')
                                          ],
                                          help_text='Geben sie hier die Sekunden an, an dem das'
                                                    'Gebäude im Video erscheint'
                                                    '(Wird mit den Minuten verbunden')

    def get_timestamps_by_video(self, vid):
        # pylint: disable= no-member
        """
        Getting all timestamp in a video filtered by the id of the video
        :param vid: id of the video
        :return: QuerySet of the filtered timestamps
        """
        return self.objects.filter(video=vid)

    def get_timestamps_by_building(self, build):
        # pylint: disable= no-member
        """
        Getting all timestamp for the given building filtered by the id of the building
        :param build: id of the building
        :return: QuerySet of the filtered timestamps
        """
        return self.objects.filter(building=build)
