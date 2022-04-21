from django.db import models


# Create your models here.
class Analytic(models.Model):
    """
    Model for analytics.
    """
    site_url = models.CharField(verbose_name="URL", editable=False, max_length=500)
    name = models.CharField(verbose_name="Bezeichnung", editable=False, max_length=100)
    month = models.PositiveIntegerField(verbose_name="Für Monat", editable=False, default=0)
    year = models.PositiveIntegerField(verbose_name="Für Jahr", editable=False, default=0)
    visits = models.PositiveIntegerField(verbose_name="Anzahl der Besuche", editable=False, default=0)

