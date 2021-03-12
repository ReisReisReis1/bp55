"""
Configurations for the Database Models for the App 'materials_page'
"""
from django.core.exceptions import ValidationError
from django.db import models


def validate_pdf_extension(filename):
    import os
    ext = os.path.splitext(filename.name)[1]
    if ext != ".pdf":
        raise ValidationError("Es sind nur Datein mit Endung .pdf erlaubt.")


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

    def get_name(self, category_name):
        # pylint: disable= no-member
        """
        :param category_name:  name to fetch the correct category
        :return: name of the category
        """
        try:
            category = self.objects.get(name=category_name),
            return category.name
        except Category.DoesNotExist:
            Category.DoesNotExist


class Material(models.Model):
    # pylint: disable = too-few-public-methods
    """
    name: short decription of what the file is about
    file: the material file
    category: category of the file
    """

    class Meta:
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Materialien'
        verbose_name_plural = 'Materialien'

    name = models.CharField(verbose_name='Titel', max_length=1000,
                            help_text='Bezeichnung der Datei')
    file = models.FileField(verbose_name='Datei', upload_to='material/',
                            help_text="Datei hochladen.", validators=[validate_pdf_extension])
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


