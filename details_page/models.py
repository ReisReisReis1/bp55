"""
Configurations for the Database Models for the App 'details_page'
"""

# pylint: disable=import-error, relative-beyond-top-level, raise-missing-from
from django.db import models
from django.core.exceptions import ValidationError
from . import country_codes


def validate_url_conform_str(string):
    """
    Validates input for not having "&" and "?" in it.
    :param string: the input string
    :return: None or ValidationError
    """
    if "&" in string or "?" in string or '\'' in string or '\"' in string:
        raise ValidationError(
            message="Diese Eingabe darf nicht die Zeichen \"&\", \"?\" und alle Art von " +
                    "Anführungszeichen enthalten.")


def validate_color_code(code):
    """
    Validator for color Code in Era.
    :param code: the code to test
    :return: None or ValidationError
    """
    for sign in code:
        if sign not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e",
                        "f", "A", "B", "C", "D", "E", "F"]:
            raise ValidationError(
                message="Bitte einen gültigen Code im Hex-Format einfügen: " +
                        "Nur Hex-Zeichen: 0-9, a-func und A-F.")
    if len(code) != 6:
        raise ValidationError(
            message="Bitte einen gültigen Code im Hex-Format einfügen: " +
                    "Muss genau 6 Zeichen lang sein.")


class Era(models.Model):
    # pylint : disable= too-few-public-methods
    """
    Era Model.
    year_from: Beginning year of era
    year_from_BC_or_AD: BC or AD for year_from
    year_to: Ending year of era
    year_to_BC_or_AD: BC or AD for year_to
    visible_on_video_page: if the era should be visible on the video page
    color_code: hex color code for the era
    """

    class Meta:
        # pylint: disable = too-few-public-methods
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Epoche'
        verbose_name_plural = 'Epochen'

    name = models.CharField(verbose_name='Name', max_length=100, choices=[
        ('Bronzezeit', 'Bronzezeit'), ('Frühe Eisenzeit', 'Frühe Eisenzeit'),
        ('Archaik', 'Archaik'),
        ('Klassik', 'Klassik'), ('Hellenismus', 'Hellenismus'),
        ('Kaiserzeit', 'Kaiserzeit'),
        ('Spätantike', 'Spätantike'),
        ('Rezeption', 'Rezeption'),
    ], help_text="Epoche auswählen.", unique=True, null=False, blank=False)
    year_from = models.PositiveIntegerField(verbose_name='Anfangsdatum',
                                            help_text="Jahr des Beginns der Epoche eingeben.",
                                            blank=True, null=True)
    year_from_BC_or_AD = models.CharField(verbose_name='Anfangsdatum v.Chr./n.Chr.?', max_length=7,
                                          help_text="Jahr des Beginns: v.Chr. bzw. n.Chr. "
                                                    "auswählen.",
                                          choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")],
                                          default="v.Chr.",
                                          null=True, blank=True)
    year_to = models.PositiveIntegerField(verbose_name='Enddatum',
                                          help_text="Jahr des Endes der Epoche eingeben.",
                                          blank=True, null=True)
    year_to_BC_or_AD = models.CharField(verbose_name='Enddatum v.Chr/n.Chr.?', max_length=7,
                                        help_text="Jahr des Endes: v.Chr. bzw. n.Chr. auswählen.",
                                        choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")],
                                        default="v.Chr.",
                                        null=True, blank=True)
    visible_on_video_page = models.BooleanField(verbose_name='Sichtbar auf Staffelseite?',
                                                default=True, help_text="""Angeben ob die Epoche
                                                auf der 'Staffeln' Seite sichtbar sein soll.""")
    color_code = models.CharField(verbose_name='Farbkodierung',
                                  max_length=6, help_text="""Hier 6. stelligen Hex-Farbcode für die
                                  Epoche eingeben (ohne das führende '#')(z.B.: #ffffff = Weiß).""",
                                  default="ffffff", validators=[validate_color_code])

    def __str__(self):
        """
        Name for Eras for the admin interface.
        :return: eras name
        """
        return str(self.name)

    def get_year_as_signed_int(self):
        """
        Getting the dates of an era as signed int
        :return: list with two elements: new_list[0] start date, new_list[1] end date
        """
        new_list = [0, 0]
        date = 9999
        if self.year_from is not None:
            # Checking for the self start date if it is before or after the birth of christ
            if self.year_from_BC_or_AD == 'v.Chr.':
                date = -1 * int(self.year_from)
            elif self.year_from_BC_or_AD == 'n.Chr.':
                date = int(self.year_from)
        new_list[0] = date
        date = 9999
        if self.year_to is not None:
            # Checking for the self end date if it is before or after the birth of christ
            if self.year_to_BC_or_AD == 'v.Chr.':
                date = -1 * int(self.year_to)
            elif self.year_to_BC_or_AD == 'n.Chr.':
                date = int(self.year_to)
        new_list[1] = date
        return new_list

    def get_year_as_str(self):
        """
        Getting the start year as string
        Building a  string with the years that are not null, for both, year_from and year_to
        :return: The
        """
        start = ''
        end = ''
        if self.year_from is not None:
            year_from = str(self.year_from)
            # n.Chr. as default
            bc_ad_from = ' ' + str(
                self.year_from_BC_or_AD) if self.year_from is not None else 'v.Chr.'
            start = year_from + bc_ad_from
            if self.year_to is not None:
                year_to = str(self.year_to)
                bc_ad_to = ' ' + str(
                    self.year_to_BC_or_AD) if self.year_to_BC_or_AD is not None else 'v.Chr.'
                end = ' - ' + year_to + bc_ad_to

        return start + end


class Building(models.Model):
    # pylint: disable = too-many-public-methods, no-member
    """
    Database model for buildings. Will be used in detail page, but also in timeline and filter page.
    name: name of the building
    description: a short description of the building
    city: city in which the building is located
    region: region in which the buildind is located
    country: country in which the building is located
    year_from: date on which construction began
    year_from_BC_or_AD: BC/AD switcher for date_from
    year_to: date on which construction ended
    year_to_BC_or_AD: BC/AD switcher for date_to
    year_ca: if the date is exact or an estimation
    year_century: if the given date is just a century-approximation and not an exact year
    architect: architect of the building
    context: context/type of the building
    builder: builder of the building
    construction_type: construction type of the building
    design: design/shape of the building
    function: function that the building fulfills
    length: length of the building
    width: width of the building
    height: height of the building
    circumference: circumference of the building ( for circular buildings)
    area: surface area of the building
    column_order: column order of the building
    construction: construction of the building
    material: material of the building
    literature: further literature about the building
    links: links for further reading
    era: era in which the building was built
    """

    class Meta:
        # pylint: disable = too-few-public-methods, raise-missing-from
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Gebäude'
        verbose_name_plural = 'Gebäude'

    name = models.CharField(verbose_name='Name', max_length=100,
                            help_text="Namen des Bauwerks eingeben (max. 100 Zeichen).",
                            validators=[validate_url_conform_str])
    description = models.TextField(verbose_name='Beschreibung', max_length=1000,
                                   help_text="Beschreibung des Gebäudes angeben (max. 1000 Zeichen",
                                   null=True, blank=True, editable=True)
    city = models.CharField(verbose_name='Stadt', max_length=100,
                            help_text="Stadt des Bauwerks eingeben (max. 100 Zeichen).",
                            null=True, blank=True, validators=[validate_url_conform_str])
    region = models.CharField(verbose_name='Region', max_length=100,
                              help_text="Region des Bauwerks eingeben (max. 100 Zeichen).",
                              null=True, blank=True, validators=[validate_url_conform_str])
    country = models.CharField(verbose_name='Land', max_length=100,
                               help_text="Hier Land des Bauwerks auswählen (Tipp:"
                                         "Zum Suchen Kürzel "
                                         "auf der Tastatur eingeben).",
                               choices=country_codes.country_codes_as_tuple_list,
                               default="Griechenland", null=True, blank=True,
                               validators=[validate_url_conform_str])
    year_from = models.PositiveIntegerField(
        verbose_name='Baubeginn',
        help_text="Jahr des Baubeginns eingeben. Wenn nicht gesetzt, "
                  "erscheint das Gebäude am Ende der Zeitachse.",
        null=True, blank=True)
    year_from_BC_or_AD = models.CharField(verbose_name='Baubeginn v.Chr./n.Chr.?', max_length=7,
                                          help_text="Jahr des Baubeginns: v.Chr. bzw. n.Chr. "
                                                    "auswählen.",
                                          choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")],
                                          default="v.Chr.",
                                          null=True, blank=True)
    year_to = models.PositiveIntegerField(verbose_name='Bauende',
                                          help_text="Jahr des Bauendes eingeben.",
                                          null=True, blank=True)
    year_to_BC_or_AD = models.CharField(verbose_name='Bauende v.Chr/n.Chr.?', max_length=7,
                                        help_text="Jahr des Bauendes: v.Chr. bzw. n.Chr. "
                                                  "auswählen.",
                                        choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")],
                                        default="v.Chr.",
                                        null=True, blank=True)
    year_century = models.BooleanField(verbose_name='Jahrhundertangaben?', default=False,
                                       help_text="Sind die Daten Jahrhundert Angaben?")
    year_ca = models.BooleanField(verbose_name='ungefähre Jahresangabe?', default=False,
                                  help_text="ca. zum Datum hinzufügen (für ungenaue Datumsangaben)"
                                            ".")
    era = models.ForeignKey(verbose_name='Epoche', to=Era, on_delete=models.SET_NULL,
                            null=True, blank=True)
    architect = models.CharField(verbose_name='Architekt', max_length=100,
                                 help_text="Architekt des Bauwerks eingeben (max. 100 Zeichen).",
                                 null=True, blank=True, validators=[validate_url_conform_str])
    context = models.CharField(verbose_name='Kontext', max_length=100,
                               help_text="Kontext des Bauwerks eingeben (Haus, Siedlung, "
                                         "öfftl. Platz etc., max. 100 Zeichen)",
                               null=True, blank=True, validators=[validate_url_conform_str])
    builder = models.CharField(verbose_name='Bauherr', max_length=100,
                               help_text="Bauherren des Bauwerks eingeben (max. 100 Zeichen).",
                               null=True, blank=True, validators=[validate_url_conform_str])
    construction_type = models.CharField(verbose_name='Bautyp', max_length=100,
                                         help_text="Bautyp des Bauwerks eingeben "
                                                   "(max. 100 Zeichen).",
                                         null=True, blank=True,
                                         validators=[validate_url_conform_str])
    design = models.CharField(verbose_name='Bauform', max_length=100,
                              help_text="Bauform des Bauwerks angeben. (max. 100 Zeichen)",
                              null=True, blank=True, validators=[validate_url_conform_str])
    function = models.CharField(verbose_name='Funktion', max_length=100,
                                help_text="Gattung/Funktion des Bauwerks eingeben "
                                          "(max. 100 Zeichen).",
                                null=True, blank=True, validators=[validate_url_conform_str])
    length = models.FloatField(verbose_name='Länge',
                               help_text="Länge des Bauwerks eingeben (falls vorhanden, in m).",
                               null=True, blank=True)
    width = models.FloatField(verbose_name='Breite',
                              help_text="Breite des Bauwerks eingeben (falls vorhanden, in m).",
                              null=True, blank=True)
    height = models.FloatField(verbose_name='Höhe',
                               help_text="Höhe des Bauwerks eingeben (falls vorhanden, in m).",
                               null=True, blank=True)
    circumference = models.FloatField(
        verbose_name='Durchmesser',
        help_text="Durchmesser des Bauwerks eingeben (falls vorhanden).",
        null=True, blank=True)
    area = models.FloatField(verbose_name='Fläche',
                             help_text="Fläche des Bauwerks eingeben (falls vorhanden, in ha).",
                             null=True, blank=True)
    column_order = models.CharField(verbose_name='Säulenordnung', max_length=100,
                                    help_text="Säulenordnung des Gebäudes eingeben "
                                              "(max. 100 Zeichen).",
                                    null=True, blank=True,
                                    validators=[validate_url_conform_str])
    construction = models.CharField(verbose_name='Konstruktion', max_length=100,
                                    help_text="Konstruktion des Bauwerks eingeben"
                                              "(z.B. Massivbau, etc., falls "
                                              "vorhanden, max. 100 Zeichen)",
                                    null=True, blank=True,
                                    validators=[validate_url_conform_str])
    material = models.CharField(verbose_name='Material', max_length=100,
                                help_text="Material des Bauwerks eingeben (max. 100 Zeichen).",
                                null=True, blank=True, validators=[validate_url_conform_str])
    literature = models.TextField(verbose_name='Literatur', max_length=1000,
                                  help_text="Literatur zum Gebäude angeben (max. 1000 Zeichen).",
                                  null=True, blank=True)
    links = models.TextField(verbose_name='Links', max_length=1000,
                             help_text="Weiterführende Links zum Gebäude "
                                       "angeben (max. 1000 Zeichen)."
                                       "Es werden nur Links im folgenden Format erkannt:"
                                       "https://moodle.tu-darmstadt.de/my/", default="", null=True,
                             blank=True)

    # pylint: disable = raise-missing-from
    def __str__(self):
        """
        Name for the admin interface
        :return: the name of a Building
        """
        return str(self.name)

    def get_name(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: name of the building
        """
        try:
            building = self.objects.get(pk=building_id)
        except Building.DoesNotExist:
            raise Building.DoesNotExist
        return building.name

    def get_era(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: era of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.era
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_description(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: description of the building
        """
        try:
            building = self.objects.get(pk=building_id)
        except Building.DoesNotExist:
            raise Building.DoesNotExist
        return building.description

    def get_city(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: city in which the building is located
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.city
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_region(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: city in which the building is located
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.region
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_country(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: country in which the building is located
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.country
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_year_from(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: year on which construction began
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.year_from
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_year_from_bc_or_ad(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: if year_from is BC or AD
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.year_from_BC_or_AD
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_year_to(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: year on which construction began
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.year_to
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_year_to_bc_or_ad(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: if year from is BC or AD
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.year_to_BC_or_AD
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_year_ca(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: if the year is an exact specification or not
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.year_ca
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_year_century(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: if the date is a century-approximation
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.year_century
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_architect(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: architect of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.architect
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_context(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: context/type of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.context
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_builder(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: builder of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.builder
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_construction_type(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: construction type of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.construction_type
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_design(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: design/shape of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.design
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_function(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: function of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.function
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_length(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: length of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.length
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_width(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: width of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.width
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_height(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: height of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.height
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_circumference(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: circumference of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.circumference
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_area(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: area of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.area
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_column_order(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: column order of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.column_order
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_construction(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: construction of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.construction
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_material(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: material of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.material
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_literature(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: further literature about the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.literature
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_links(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: list of links for further reading
        """
        try:
            building = self.objects.get(pk=building_id)
            # Splits the strings in the list at ; and ,
            txt = building.links
            # Splitting the txt at ","
            lst = txt.split(", ")
            # Getting back all Elements that are not equal(__ne__) to ''
            return list(filter(''.__ne__, lst))
        except Building.DoesNotExist:
            raise Building.DoesNotExist

    def get_year_as_signed_int(self):
        """
        Getting the dates of an building as signed int
        :return: list with two elements: new_list[0] start date, new_list[1] end date
        """
        new_list = [0, 0]
        date = 9999
        if self.year_from is not None:
            # Checking for the self start date if it is before or after the birth of christ
            if self.year_from_BC_or_AD == 'v.Chr.':
                date = -1 * int(self.year_from)
                if self.year_century and date != 0:
                    date = date * 100 + 50
            elif self.year_from_BC_or_AD == 'n.Chr.':
                date = int(self.year_from)
                if self.year_century and date != 0:
                    date = date * 100 - 50
        new_list[0] = date
        date = 9999
        if self.year_to is not None:
            # Checking for the self end date if it is before or after the birth of christ
            if self.year_to_BC_or_AD == 'v.Chr.':
                date = -1 * int(self.year_to)
                if self.year_century and self.year_to != 0:
                    date = date * 100 + 50
            elif self.year_to_BC_or_AD == 'n.Chr.':
                date = int(self.year_to)
                if self.year_century and date != 0:
                    date = date * 100 - 50
        new_list[1] = date
        return new_list

    def get_year_as_str(self):
        """
        Getting the start year plus end year as string
        """
        century = '. Jh.' if self.year_century else ''
        circa = 'ca. ' if self.year_ca else ''
        start = ''
        end = ''
        if self.year_from is not None:
            year_from = str(self.year_from)
            # default n.Chr.
            bc_ad_from = ' ' + str(
                self.year_from_BC_or_AD) if self.year_from is not None else 'v.Chr.'
            start = circa + year_from + century + bc_ad_from
            if self.year_to is not None:
                year_to = str(self.year_to)
                # default n.Chr.
                bc_ad_to = ' ' + str(
                    self.year_to_BC_or_AD) if self.year_to_BC_or_AD is not None else 'v.Chr.'
                end = ' - ' + circa + year_to + century + bc_ad_to

        return start + end

    def get_thumbnail(self):
        """
        Getting the thumbnail for this building
        """
        try:
            thumbnail = Picture.objects.get(building=self.id, usable_as_thumbnail=True)
        except Picture.DoesNotExist:
            thumbnail = None
        except Picture.MultipleObjectsReturned:
            thumbnail = Picture.objects.filter(building=self.id, usable_as_thumbnail=True)[0]
        return thumbnail


class Blueprint(models.Model):
    # pylint : disable = too-few-public-methods
    """
    name: Name of the blueprint
    description: description for the blueprint
    blueprint: the actual blueprint picture file.
    width: width of the blueprint picture
    height: height of the blueprint picture
    building: the building it refers to.
    """

    class Meta:
        # pylint: disable=too-few-public-methods
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Bauplan'
        verbose_name_plural = 'Baupläne'

    name = models.CharField(verbose_name='Name', max_length=100,
                            help_text="Titel des Bauplans eingeben (max. 100 Zeichen).")
    description = models.TextField(verbose_name='Beschreibung', max_length=1000,
                                   help_text="Beschreibung des Bildes eingeben "
                                             "(max. 1000 Zeichen).",
                                   null=True, blank=True, editable=False)
    blueprint = models.ImageField(
        verbose_name='Bauplan',
        help_text="Auf \"Durchsuchen\" drücken um einen Bauplan hochzuladen.",
        upload_to="blueprint/",
        width_field="width", height_field="height")
    width = models.IntegerField(editable=False, default=0)
    height = models.IntegerField(editable=False, default=0)
    building = models.ForeignKey(verbose_name='Gebäude', to=Building,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        """
        Name for the admin interface
        :return: the name of a Blueprint
        """
        return str(self.name)

    def get_blueprint_for_building(self, wanted_building):
        # pylint: disable= no-member
        """
        Getting a QuerySet of blueprints for the given building
        :param wanted_building: ID to fetch the correct building
        :return: QuerySet of blueprints for given building or empty QuerySet
        """
        blueprints = self.objects.filter(building=wanted_building)
        return blueprints


class Picture(models.Model):
    # pylint : disable= too-few-public-methods
    """
    Picture Model: Will be used to save Pictures for all-over the website, except
    thumbnails in videos and blueprints.
    name: Name of the Picture
    description: description for the picture.
    picture: the actual picture file.
    width: width of the pic
    height: height of the pic
    building: the building it refers to.
    usable_as_thumbnail: If this picture can be used as thumbnail for the building on the timeline,
        search and filter results.
    """

    class Meta:
        # pylint: disable = too-few-public-methods
        """
        Meta data for the model
        In this case the singular and plural name that will be seen in the admin interface
        """
        verbose_name = 'Bild'
        verbose_name_plural = 'Bilder'

    name = models.CharField(verbose_name='Name', max_length=100,
                            help_text="Titel des Bildes eingeben (max. 100 Zeichen).")
    description = models.TextField(verbose_name='Beschreibung', max_length=1000,
                                   help_text="Beschreibung des Bildes eingeben "
                                             "(max. 1000 Zeichen).",
                                   null=True, blank=True, editable=False)
    picture = models.ImageField(
        verbose_name='Bild',
        help_text="Auf \"Durchsuchen\" drücken um ein Bild hochzuladen.",
        upload_to="pics/",
        width_field="width", height_field="height")
    width = models.IntegerField(editable=False, default=0)
    height = models.IntegerField(editable=False, default=0)
    building = models.ForeignKey(verbose_name='Gebäude', to=Building,
                                 null=True, blank=True, on_delete=models.SET_NULL)
    usable_as_thumbnail = models.BooleanField(
        verbose_name='Thumbnail?', default=False,
        help_text="Anwählen wenn das Bild als Thumbnail "
                  "(Vorschaubild) für sein Bauwerk in der Zeitachse, "
                  "der Bauwerke-Seite, und in den Suchergebnissen "
                  "erscheinen darf. Bei mehreren möglichen "
                  "Vorschaubildern für ein Bauwerk "
                  "wird zufällig eins ausgewählt.")

    def __str__(self):
        """
        Name for the admin interface
        :return: the name of a Picture
        """
        return str(self.name)

    def get_picture_for_building(self, wanted_building):
        # pylint: disable= no-member
        """
        Getting a QuerySet of Pictures for the given building
        :param wanted_building: ID to fetch the correct building
        :return: QuerySet of Pictures for given building or empty QuerySet
        """
        pictures = self.objects.filter(building=wanted_building)
        return pictures
