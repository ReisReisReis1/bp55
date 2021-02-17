"""
Configurations for the Database Models for the App 'details_page'
"""

import re
from django.db import models
from django.core.exceptions import ValidationError
# pylint: disable=import-error
from . import country_codes


def validate_url_conform_str(string):
    """
    Validates input for not having "&" and "?" in it.
    :param string: the input string
    :return: None or ValidationError
    """
    if "&" in string or "?" in string or '\'' in string or '\"' in string:
        raise ValidationError(
            message="Diese Eingabe darf nicht die Zeichen \"&\", \"?\" und alle Art von "
                    "Anführungszeichen enthalten.")


def validate_color_code(code):
    """
    Validator for color Code in Era.
    :param code: the code to test
    :return: None or ValidationError
    """
    for sign in code:
        if sign not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d",
                        "e",
                        "f", "A", "B", "C", "D", "E", "F"]:
            raise ValidationError(message="Bitte einen gültigen Code im Hex-Format einfügen: "
                                          "Nur Hex-Zeichen: 0-9, a-f und A-F.")
        if len(code) != 6:
            raise ValidationError(message="Bitte einen gültigen Code im Hex-Format einfügen: "
                                          "Muss genau 6 Zeichen lang sein.")


class Era(models.Model):
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
        verbose_name = 'Epoche'
        verbose_name_plural = 'Epochen'

    name = models.CharField(verbose_name='Name', max_length=100, choices=[
        ('Bronzezeit', 'Bronzezeit'), ('Frühzeit', 'Frühzeit'), ('Archaik', 'Archaik'),
        ('Klassik', 'Klassik'), ('Hellenismus', 'Hellenismus'),
        ('Königszeit', 'Königszeit'), ('Republik', 'Republik'),
        ('Frühe Kaiserzeit', 'Frühe Kaiserzeit'),
        ('Mittlere Kaiserzeit', 'Mittlere Kaiserzeit'),
        ('Späte Kaiserzeit', 'Späte Kaiserzeit'),
        ('Spätantike', 'Spätantike'),
        ('Sonstiges', 'Sonstiges'),
    ], default='Sonstiges', help_text="Epoche auswählen.", unique=True)
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
    year_to_BC_or_AD = models.CharField(verbose_name='Endatum v.Chr/n.Chr.?', max_length=7,
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

    def get_year_of_item_as_signed_int(self):
        """
        Inner helper to sorting the years.
        About the try/except: You can define an Era without an year.
        This leads to following problem:
        You can not sort Eras by year if there is one without an year.
        In line 29 or 31 we try to get the
        year as an Int. This will raise the TypeError,
        if this Era don't has a year (or the year is setto None to be exact).
        Therefore we except this error, and return 2021, which is higher than
        every year in the Database (limited to max_years (currently 1400)).
        :return: the year of the era(beginning year)
        """
        try:
            if self.year_from_BC_or_AD == "v.Chr.":
                return -1 * int(self.year_from)
            else:
                return int(self.year_from)
        except TypeError:
            # If era has no year return big int, so it will be listed last.
            return 9999999999999999999


class Building(models.Model):
    # pylint: disable = too-many-public-methods
    """
    Database model for buildings. Will be used in detail page, but also in timeline and filter page.
    name: name of the building
    description: a short description of the building
    city: city in which the building is located
    region: region in which the buildind is located
    country: country in which the building is located
    date_from: date on which construction began
    date_from_BC_or_AD: BC/AD switcher for date_from
    date_to: date on which construction ended
    date_to_BC_or_AD: BC/AD switcher for date_to
    date_ca: if the date is exact or an estimation
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
        verbose_name = 'Gebäude'
        verbose_name_plural = 'Gebäude'

    name = models.CharField(verbose_name='Name', max_length=100,
                            help_text="Namen des Bauwerks eingeben (max. 100 Zeichen).",
                            validators=[validate_url_conform_str])
    description = models.TextField(verbose_name='Beschreibung', max_length=1000,
                                   help_text="Beschreibung des Gebäudes angeben (max. 1000 Zeichen",
                                   null=True, blank=True, editable=False)
    city = models.CharField(verbose_name='Stadt', max_length=100,
                            help_text="Stadt des Bauweks eingeben (max. 100 Zeichen).",
                            null=True, blank=True, validators=[validate_url_conform_str])
    region = models.CharField(verbose_name='Region', max_length=100,
                              help_text="Region des Bauwerks eingeben (max. 100 Zeichen).",
                              null=True, blank=True, validators=[validate_url_conform_str])
    country = models.CharField(verbose_name='Land', max_length=100,
                               help_text="Hier Land des Bauwerks auswählen (Tipp:"
                                         "Zum Suchen Kürzel"
                                         "auf der Tastatur eingeben).",
                               choices=country_codes.country_codes_as_tuple_list,
                               default="Griechenland", null=True, blank=True,
                               validators=[validate_url_conform_str])
    date_from = models.PositiveIntegerField(
        verbose_name='Baubeginn',
        help_text="Jahr des Baubeginns eingeben. Wenn nicht gesetzt, "
                  "erscheint das Gebäude nicht auf der Zeitachse.",
        null=True, blank=True)
    date_from_BC_or_AD = models.CharField(verbose_name='Baubeginn v.Chr./n.Chr.?', max_length=7,
                                          help_text="Jahr des Baubeginns: v.Chr. bzw. n.Chr. "
                                                    "auswählen.",
                                          choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")],
                                          default="v.Chr.",
                                          null=True, blank=True)
    date_to = models.PositiveIntegerField(verbose_name='Bauende',
                                          help_text="Jahr des Bauendes eingeben.",
                                          null=True, blank=True)
    date_to_BC_or_AD = models.CharField(verbose_name='Bauende v.Chr/n.Chr.?', max_length=7,
                                        help_text="Jahr des Bauendes: v.Chr. bzw. n.Chr. "
                                                  "auswählen.",
                                        choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")],
                                        default="v.Chr.",
                                        null=True, blank=True)
    date_century = models.BooleanField(verbose_name='Jahrhundertangaben?', default=False,
                                       help_text="Sind die Daten Jahrhundert Angaben?")
    date_ca = models.BooleanField(verbose_name='ungefähre Datumsangabe?', default=False,
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
    links = models.TextField(verbose_name='Links', max_length=1000, help_text="Weiterführende Links zum Gebäude "
                             "angeben (max. 1000 Zeichen).", default="", null=True, blank=True)

    def __str__(self):
        """
        Name for the admin interface
        :return: the name of a Building
        """
        try:
            return str(self.name)
        except Building.MultipleObjectsReturned:
            return Building.MultipleObjectsReturned

    def get_name(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: name of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.name
        except Building.DoesNotExist:
            return Building.DoesNotExist

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
            return Building.DoesNotExist

    def get_description(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: description of the building
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.description
        except Building.DoesNotExist:
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

    def get_date_from(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: date on which construction began
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.date_from
        except Building.DoesNotExist:
            return Building.DoesNotExist

    def get_date_from_bc_or_ad(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: if date_from is BC or AD
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.date_from_BC_or_AD
        except Building.DoesNotExist:
            return Building.DoesNotExist

    def get_date_to(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: date on which construction began
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.date_to
        except Building.DoesNotExist:
            return Building.DoesNotExist

    def get_date_to_bc_or_ad(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: if date_from is BC or AD
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.date_to_BC_or_AD
        except Building.DoesNotExist:
            return Building.DoesNotExist

    def get_date_ca(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: if the date is an exact specification or not
        """
        try:
            building = self.objects.get(pk=building_id)
            return building.date_ca
        except Building.DoesNotExist:
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

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
            return Building.DoesNotExist

    def get_links(self, building_id):
        # pylint: disable= no-member
        """
        :param building_id: ID to fetch the correct building
        :return: list of links for further reading
        """
        try:
            building = self.objects.get(pk=building_id)
            """
            Splits the strings in the list at ; and ,
            """
            txt = building.links
            # Splitting the txt at ","
            lst = txt.split(", ")
            # Getting back all Elements that are not equal(__ne__) to ''
            return list(filter(''.__ne__, lst))
        except Building.DoesNotExist:
            return Building.DoesNotExist


class Blueprint(models.Model):
    """
    name: Name of the blueprint
    description: description for the blueprint
    blueprint: the actual blueprint picture file.
    width: width of the blueprint picture
    height: height of the blueprint picture
    building: the building it refers to.
    """

    class Meta:
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
        try:
            blueprints = self.objects.filter(building=wanted_building)
            return blueprints
        except Building.DoesNotExist:
            return Building.DoesNotExist


class Picture(models.Model):
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
        try:
            pictures = self.objects.filter(building=wanted_building)
            return pictures
        except Building.DoesNotExist:
            return Building.DoesNotExist
