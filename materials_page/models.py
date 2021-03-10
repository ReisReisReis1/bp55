"""
Configurations for the Database Models for the App 'materials_page'
"""

from django.db import models


class Category(models.Model):
    # pylint: disable = too-many-public-methods
    """
    name: the catgeorys name
    """

    class Meta:
        verbose_name = 'Kategorie'
        verbose_name_plural = 'Kategorien'

    name = models.CharField(verbose_name='Titel', max_length=1000, help_text='Bezeichnung der Kategorie')

    def __str__(self):
        """
        Name for the admin interface
        :return: the name of the category
        """
        return str(self.name)


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
    category = models.ForeignKey(verbose_name='Kategorie', to=Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        """
        Name for the admin interface
        :return: the name of a Building
        """
        return str(self.name)

    def get_category(self):
        """
        :return: category name
        """
        try:
            return self.category.name
        except Category.DoesNotExist:
            return Category.DoesNotExist
        except Category.MultipleObjectsReturned:
            Category.MultipleObjectsReturned


