from django.db import models
from django.core.exceptions import ValidationError

"""
Configurations for the Database Models for the App 'start'
"""


class IntroTexts(models.Model):
    """
    Texte für die Intro-Seite.
    :param: intro_text: The text for the intro site.
    :timeline_card_text: Text for the timeline card.
    :buildings_card_text: Text for the buildings card.
    :video_card_text: Text for the video card.
    """

    intro_text = models.TextField(verbose_name="Intro-Text", max_length=5000,
                                  help_text="Allgemeiner Text für die Intro-Seite (max. 5000 Zeichen).")
    timeline_card_text = models.TextField(verbose_name="Zeitachsen Karten Text", max_length=250,
                                          help_text="Text für die Zeitachsen Karte (max. 250 Zeichen).")
    buildings_card_text = models.TextField(verbose_name="Bauwerke Karten Text", max_length=250,
                                           help_text="Text für die Bauwerke Karte (max. 250 Zeichen).")
    video_card_text = models.TextField(verbose_name="Video Karten Text", max_length=250,
                                       help_text="Text für die Video Karte (max. 250 Zeichen).")

    def __str__(self):
        """
        Name for the admin interface
        :return: "Texte für die Introseite"
        """
        return "Texte für die Introseite"

    def save(self, *args, **kwargs):
        # pylint: disable = signature-differs
        """
        Makes sure that its not possible to create multiple instances of IntroTexts
        overrides the save method
        :param args: is needed for object creation
        :param kwargs: is needed for object creation
        :return: returns an error if you try to make multiple instances of IntroTexts
        """
        # pylint: disable = no-member
        if not self.pk and IntroTexts.objects.exists():
            # if you'll not check for self.pk then error will also raised in update of exists model
            raise ValidationError(
                'Es kann nur eine Instanz von Intro Texten geben. Bitte ändern Sie die schon'
                ' existierende Instanz, oder löschen Sie diese, bevor Sie eine neue erzeugen.')
        # pylint: disable = super-with-arguments
        return super(IntroTexts, self).save(*args, **kwargs)

    class Meta:
        """
        Set names for admin interface.
        """

        verbose_name = "Intro-Seiten Texte"
        verbose_name_plural = "Intro-Seiten Texte"

