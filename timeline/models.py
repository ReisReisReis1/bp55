"""
Configurations for the Database Models for the App 'timeline'
"""
# pylint: disable = no-name-in-module, import-error
from django.db import models
from details_page.models import Era


class HistoricDate(models.Model):
    # pylint: disable = too-few-public-methods, no-member
    """
    Database model for historic dates, that will be used in the timeline.
    year: the year for the historic happening, set negative ones for B.C. and positive ones for A.D.
    title: Title for the historic happening
    infos: a short abstract text giving information about the historic happening
    """

    class Meta:
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Historisches Datum'
        verbose_name_plural = 'Historische Daten'

    year = models.PositiveIntegerField(verbose_name='Jahr', help_text=
                                        "Hier das Jahr des Ereignisses einfügen. "
                                        "Falls es ein genaueres Datum gibt, wird diese angezeigt.",
                                       null=True, blank=True)
    exacter_date = models.DateField(verbose_name='Exaktes Datum', null=True, blank=True,
                                    help_text="Falls das Ereignis ein genaueres Datum hat, "
                                              "hier eingeben. "
                                              "Diese Feld unterstützt zusätzlich zur Jahreszahl "
                                              "(wie obendrüber), "
                                              "Monats- und Tagesangaben, "
                                              "es kann aber auch leer bleiben. "
                                              "Falls diese und die Jahreszahl gesetzt sind, "
                                              "wird dieses genauere Datum das "
                                              "sein, dass angezeigt wird. "
                                              "ACHTUNG: Jahreszahlen bitte vierstellig eingeben: "
                                              "Das Jahr '17' wird sonst automatisch zu '2017' "
                                              "erweitert, "
                                              "möchte man das Jahr 17 haben, muss man '0017' "
                                              "eingeben.")
    year_BC_or_AD = models.CharField(verbose_name='vor oder nach Christigeburt?', max_length=7,
                                     help_text="Jahr des Ereignisses: "
                                               "v.Chr. bzw. n.Chr. auswählen.",
                                     choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")],
                                     default="v.Chr.")
    year_century = models.BooleanField(verbose_name='Jahrhundert', default=False,
                                       help_text="Sind die Daten Jahrhundert Angaben?")
    year_ca = models.BooleanField(verbose_name='ungefähres Datum?', default=False,
                                  help_text="ca. zum Datum hinzufügen (für ungenaue Datumsangaben)"
                                            ".")
    title = models.CharField(verbose_name='Titel', max_length=100,
                             help_text="Hier einen Titel für der Ereignis einfügen "
                                       "(max. 100 Zeichen).")
    infos = models.TextField(
        verbose_name='Information',
        help_text="Hier eine kurze Beschreibung des historischen Ereignisses einfügen "
                  "(max. 1000 Zeichen).",
        max_length=1000, editable=True)
    era = models.ForeignKey(verbose_name='Epoche', to=Era, on_delete=models.SET_NULL, null=True,
                            blank=True)

    def __str__(self):
        """
        Giving back the Historic date with titel and the date or year
        """
        return_string = str(self.title) + " (" + self.get_year_as_str() + ")"
        return return_string

    def get_year_as_signed_int(self):
        """
        Getting the year of a historic date as signed int
        :return: year as signed int or the year of the exact date as signed int
        """
        result = None
        if self.exacter_date is None and self.year is not None:
            if self.year_BC_or_AD == "v.Chr.":
                result = -1 * int(self.year)
                if self.year_century and result != 0:
                    result = result * 100 + 50
            elif self.year_BC_or_AD == 'n.Chr.':
                result = int(self.year)
                if self.year_century and result != 0:
                    result = result * 100 - 50
        elif self.exacter_date is not None:  # Getting only year of the exact date
            if self.year_BC_or_AD == "v.Chr.":
                result = -1 * int(self.exacter_date.year)
            elif self.year_BC_or_AD == 'n.Chr.':
                result = int(self.exacter_date.year)

        return [result, result]

    def get_year_as_str(self):
        """
        Getting the year as string
        """
        result = ''
        if self.exacter_date is None and self.year is not None:
            century = '. Jh.' if self.year_century else ''
            circa = 'ca. ' if self.year_ca else ''
            bc_ad = ' ' + str(self.year_BC_or_AD) if self.year_BC_or_AD is not None else 'v.Chr.'
            result = circa + str(self.year) + century + bc_ad
        elif self.exacter_date is not None:
            day = str(self.exacter_date.day)
            month = str(self.exacter_date.month)
            year = str(self.exacter_date.year)
            bc_ad = (' ' + str(self.year_BC_or_AD)) if self.year_BC_or_AD is not None else 'v.Chr.'
            result = day + '.' + month + '.' + year + bc_ad

        return result
