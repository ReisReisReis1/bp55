"""
Configurations for the Database Models for the App 'details_page'
"""

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
    ], default='Sonstiges',
                            help_text="Epoche auswählen.")
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

    def __str__(self):
        return str(self.name)

    def get_name(self, building_id):
        """
        :return: name of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.name

    def get_era(self, building_id):
        """
        :return: era of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.era

    def get_description(self, building_id):
        """
        :return: description of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.description

    def get_city(self, building_id):
        """
        :return: city in which the building is located
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.city

    def get_region(self, building_id):
        """
        :return: city in which the building is located
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.region

    def get_country(self, building_id):
        """
        :return: country in which the building is located
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.country

    def get_date_from(self, building_id):
        """
        :return: date on which construction began
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.date_from

    def get_date_from_bc_or_ad(self, building_id):
        """
        :return: if date_from is BC or AD
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.date_from_BC_or_AD

    def get_date_to(self, building_id):
        """
        :return: date on which construction began
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.date_to

    def get_date_to_bc_or_ad(self, building_id):
        """
        :return: if date_from is BC or AD
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.date_to_BC_or_AD

    def get_architect(self, building_id):
        """
        :return: architect of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.architect

    def get_context(self, building_id):
        """
        :return: context/type of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.context

    def get_builder(self, building_id):
        """
        :return: builder of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.builder

    def get_construction_type(self, building_id):
        """
        :return: construction type of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.construction_type

    def get_design(self, building_id):
        """
        :return: design/shape of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.design

    def get_function(self, building_id):
        """
        :return: function of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.function

    def get_length(self, building_id):
        """
        :return: length of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.length

    def get_width(self, building_id):
        """
        :return: width of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.width

    def get_height(self, building_id):
        """
        :return: height of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.height

    def get_circumference(self, building_id):
        """
        :return: circumference of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.circumference

    def get_area(self, building_id):
        """
        :return: area of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.area

    def get_column_order(self, building_id):
        """
        :return: column order of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.column_order

    def get_construction(self, building_id):
        """
        :return: construction of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.construction

    def get_material(self, building_id):
        """
        :return: material of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.material

    def get_literature(self, building_id):
        """
        :return: further literature about the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.literature


class Blueprint(models.Model):
    """
    Muss noch gemacht werden
    """

    class Meta:
        verbose_name = 'Bauplan'
        verbose_name_plural = 'Baupläne'

    name = models.CharField(verbose_name='Name', max_length=100,
                            help_text="Titel des Bauplans eingeben (max. 100 Zeichen).")
    description = models.TextField(verbose_name='Beschreibung', max_length=1000,
                                   help_text="Beschreibung des Bildes eingeben "
                                             "(max. 1000 Zeichen).",
                                   null=True, blank=True)
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
        return str(self.name)

    def get_blueprint_for_building(self, wanted_building):
        """
        Getting a list of blueprints for the given building
        :param wanted_building:
        :return: list of blueprints for given building or empty list
        """
        # pylint: disable= no-member
        blueprints = self.objects.filter(building=wanted_building)
        return blueprints


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
                                   null=True, blank=True)
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
        """
        Getting a List of Pictures for the given building
        :param wanted_building:
        :return: list of Pictures for given building or empty list
        """
        # pylint: disable= no-member
        pictures = self.objects.filter(building=wanted_building)
        return pictures
