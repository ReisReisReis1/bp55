"""
Configurations for the Database Models for the App 'impressum'
"""
from django.core.exceptions import ValidationError
from django.db import models


class Impressum(models.Model):
    # pylint: disable = too-many-public-methods
    """
    name: short description
    course_link: link to the lecture course
    """

    class Meta:
        verbose_name = 'Impressum'
        verbose_name_plural = 'Impressen'

    name = models.CharField(verbose_name='Bezeichnung', max_length=100, help_text='Bezeichnung zur Wiedererkennung')
    course_link = models.CharField(verbose_name='Kurslink', max_length=1000, help_text='Link zum Vorlesungskurs in'
                                    'Moodle')

    def __str__(self):
        """
        Name for the admin interface
        :return: the name of the impressum
        """
        return str(self.name)

    def save(self, *args, **kwargs):
        """
        makes sure that its not possible to create multiple instances of impressum
        ovverites the save method
        :param args: is needed for object creation
        :param kwargs: is needed for object creation
        :return: returns an error if you try to make multiple instances of Impressum
        """
        if not self.pk and Impressum.objects.exists():
            # if you'll not check for self.pk then error will also raised in update of exists model
            raise ValidationError('Es kann nur eine Instanz von Impressum geben. Bitte ändern Sie die schon'
                                  ' existierende Instanz, oder löschen Sie diese, bevor Sie eine neue erzeugen')
        return super(Impressum, self).save(*args, **kwargs)

