"""
Configurations for the Database Models for the App 'timeline'
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from details_page.models import Era
from datetime import date


"""Give the maximal year accepted for historic date objects here"""
max_year = 1400


def validate_exact_year(value):
    """
    Vaildator for the exact year.
    :param value:
    :return:
    """
    if value > date(max_year, 12, 31):
        raise ValidationError(
            message="Das eingegebene Datum ist zu hoch. Bitte etwas zwischen dem 01.01.0000 und dem 31.12."
                    + str(max_year) + " eingeben.")


class HistoricDate(models.Model):
    """
    Database model for historic dates, that will be used in the timeline.
    year: the year for the historic happening, set negative ones for B.C. and positive ones for A.D.
    title: Title for the historic happening
    infos: a short abstract text giving information about the historic happening
    """
    year = models.PositiveIntegerField(default=0000, help_text="""Hier das Jahr des Ereignisses einfügen.
                                        Falls es ein genaueres Datum gibt, wird diese angezeigt. Damit es sich ist, 
                                        dass ein Datum gegeben ist, muss dieses Feld hier aber ausgefüllt werden . """,
                                       validators=[MaxValueValidator(max_year,
                                                                     message="Diese Jahreszahl ist zu hoch. "
                                                                             + "Bitte etwas zwischen 0 und "
                                                                             + str(max_year) + " eingeben.")])
    exacter_date = models.DateField(null=True, blank=True,
                                    help_text="""Falls das Ereignis ein genaueres Datum hat, hier eingeben.
                                         Diese Feld unterstützt zusätzlich zur Jahreszahl (wie obendrüber), 
                                         Monats- und Tagesangaben, es kann aber auch leer bleiben.
                                         Falls diese und die Jahreszahl gesetzt sind, wird dieses genauere Datum das 
                                         sein, dass angezeigt wird. ACHTUNG: Jahreszahlen bitte vierstellig eingeben: 
                                         Das Jahr '17' wird sonst automatisch zu '2017' erweitert, 
                                         möchte man das Jahr 17 haben, muss man '0017' eingeben.""",
                                    validators=[validate_exact_year])
    year_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Ereignisses: v.Chr. bzw. n.Chr. auswählen.",
                                     choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.")
    title = models.CharField(max_length=100,
                             help_text="Hier einen Titel für der Ereignis einfügen (max. 100 Zeichen).")
    infos = models.TextField(
        help_text="Hier eine kurze Beschreibung des historischen Ereignisses einfügen (max. 1000 Zeichen).",
        max_length=1000)
    era = models.ForeignKey(to=Era, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.exacter_date is None:
            return str(self.title)+" ("+str(self.year)+" "+str(self.year_BC_or_AD)+")"
        else:
            return str(self.title) + " (" + str(self.exacter_date) + " " + str(self.year_BC_or_AD) + ")"





