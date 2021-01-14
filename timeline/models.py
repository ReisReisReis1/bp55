"""
Configurations for the Database Models for the App 'timeline'
"""
from django.db import models
from details_page.models import Era


class HistoricDate(models.Model):
    """
    Database model for historic dates, that will be used in the timeline.
    year: the year for the historic happening, set negative ones for B.C. and positive ones for A.D.
    title: Title for the historic happening
    infos: a short abstract text giving information about the historic happening
    """
    year = models.PositiveIntegerField(default=0000, help_text="Hier das Jahr des Ereignisses einfügen.")
    year_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Ereignisses: v.Chr. bzw. n.Chr. auswählen.",
                                     choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.")
    title = models.CharField(max_length=100,
                             help_text="Hier einen Titel für der Ereignis einfügen (max. 100 Zeichen).")
    infos = models.TextField(
        help_text="Hier eine kurze Beschreibung des historischen Ereignisses einfügen (max. 1000 Zeichen).",
        max_length=1000)
    era = models.ForeignKey(to=Era, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.title)+" ("+str(self.year)+" "+str(self.year_BC_or_AD)+")"

