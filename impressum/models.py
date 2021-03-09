"""
Configurations for the Database Models for the App 'impressum'
"""
from django.core.exceptions import ValidationError
from django.db import models


class Impressum(models.Model):
    # pylint: disable = too-few-public-methods
    """
    name: short description
    course_link: link to the lecture course
    """

    class Meta:
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Impressum'
        verbose_name_plural = 'Impressen'

    name = models.CharField(verbose_name='Bezeichnung', max_length=100,
                            help_text='Bezeichnung zur Wiedererkennung')
    course_link = models.CharField(verbose_name='Kurslink', max_length=1000,
                                   help_text='Link zum Vorlesungskurs in'
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
        # pylint: disable = no-member
        if not self.pk and Impressum.objects.exists():
            # if you'll not check for self.pk then error will also raised in update of exists model
            raise ValidationError(
                'Es kann nur eine Instanz von Impressum geben. Bitte ändern Sie die schon'
                ' existierende Instanz, oder löschen Sie diese, bevor Sie eine neue erzeugen')
        # pylint: disable = super-with-arguments
        return super(Impressum, self).save(*args, **kwargs)
