"""
Configurations for the Database Models for the App 'materials_page'
"""

from django.db import models


class Material(models.Model):
    # pylint: disable = too-many-public-methods
    """
    name: short decription of what the file is about
    file: the material file
    category: category of the file
    """

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materialien'

    name = models.CharField(verbose_name='Titel', max_length=1000, help_text='Bezeichnung der Datei')
    file = models.FileField(verbose_name='Datei', upload_to='material/',
                            help_text="Datei hochladen.")
    category = models.CharField(verbose_name='Kategorie', max_length=100, help_text='Kategorie der Datei')

    def __str__(self):
        """
        Name for the admin interface
        :return: the name of a Building
        """
        return str(self.name)

    def get_category(self, wanted_category):
        #pylint: disable= no-member
        """
        Getting all files of the given category
        :param wanted_category: the given catgeory
        :return: QuerySet of files with the given category or empty list
        """
        files = self.objects.get(category=wanted_category)




