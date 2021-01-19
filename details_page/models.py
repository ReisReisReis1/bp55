"""
Configurations for the Database Models for the App 'details_page'

def get_dimension(self, id):
        :return: Dimension of the building including length, width, height, circumference and area
        # pylint: disable= no-member
        building = self.objects.filter(pk=id)
        length_var=self.length
        width_var=self.width
        height_var=self.height
        circumference_var=self.circumference
        area_var=self.area
        dimension= Concat(V('Länge:'), 'length_var', V('Breite:'), 'width_var', V('Höhe:'), 'height_var', V('Durchmesser'), 'circumference_var', V('Fläche:'), 'area_var')
        return dimension
"""

from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from . import country_codes


"""Give max year for validation here"""
max_year = 1400


def validate_color_code(code):
    """
    Validator for color Code in Era.
    :param code: the code to test
    :return: None or ValidationError
    """
    for sign in code:
        if sign not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f",
                        "A", "B", "C", "D", "E", "F"]:
            raise ValidationError(message="Bitte einen gültigen Code im Hex-Format einfügen: "
                                          "Nur Hex-Zeichen: 0-9, a-f und A-F.")
        if len(code) != 6:
            raise ValidationError(message="Bitte einen gültigen Code im Hex-Format einfügen: "
                                          "Muss genau 6 Zeichen lang sein.")


class Era(models.Model):
    name = models.CharField(max_length=100, choices=[
        ('Bronzezeit', 'Bronzezeit'), ('Frühzeit', 'Frühzeit'), ('Archaik', 'Archaik'),
        ('Klassik', 'Klassik'), ('Helenismus', 'Helenismus'),
        ('Königszeit', 'Königszeit'), ('Republik', 'Republik'),
        ('Frühe Kaiserzeit', 'Frühe Kaiserzeit'),
        ('Mittlere Kaiserzeit', 'Mittlere Kaiserzeit'),
        ('Späte Kaiserzeit', 'Späte Kaiserzeit'),
        ('Spätantike', 'Spätantike'),
        ('Sonstiges', 'Sonstiges'),
    ], default='Sonstigedes',
                            help_text="Epoche auswählen")
    year_from = models.PositiveIntegerField(help_text="Jahr des Beginns der Epoche eingeben.", blank=True, null=True,
                                            validators=[MaxValueValidator(max_year,
                                                                          message="Diese Jahreszahl ist zu hoch."
                                                                                  + "Bitte etwas zwischen 0 und "
                                                                                  + str(max_year)
                                                                                  + " eintragen.")])
    year_from_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Beginns: v.Chr. bzw. n.Chr. auswählen.",
                                          choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.",
                                          null=True, blank=True)
    year_to = models.PositiveIntegerField(help_text="Jahr des Endes der Epoche eingeben.", blank=True, null=True,
                                          validators=[MaxValueValidator(max_year,
                                                                        message="Diese Jahreszahl ist zu hoch."
                                                                                + "Bitte etwas zwischen 0 und "
                                                                                + str(max_year)
                                                                                + " eintragen.")])
    year_to_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Endes: v.Chr. bzw. n.Chr. auswählen.",
                                        choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.",
                                        null=True, blank=True)
    visible_on_video_page = models.BooleanField(default=True, help_text="""Angeben ob die Epoche auf der 'Staffeln' 
                                                Seite sichtbar sein soll.""")
    color_code = models.CharField(max_length=6, help_text="""Hier 6. stelligen Hex-Farbcode für die Epoche eingeben 
                                                             (ohne das führende '#')(z.B.: #ffffff = Weiß).""",
                                  default="ffffff", validators=[validate_color_code])

    def __str__(self):
        return self.name


class Building(models.Model):
    """
    Database model for buildings. Will be used in detail page, but also in timeline and filter page.
    name: name of the building
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

    name = models.CharField(max_length=100, help_text="Namen des Bauwerks eingeben (max. 100 Zeichen).")
    city = models.CharField(max_length=100, help_text="Stadt des Bauweks eingeben (max. 100 Zeichen).",
                            null=True, blank=True)
    region = models.CharField(max_length=100, help_text="Region des Bauwerks eingeben (max. 100 Zeichen).",
                              null=True, blank=True)
    country = models.CharField(max_length=100, help_text="""Hier Land des Bauwerks auswählen (Tipp: Zum Suchen Kürzel 
                               auf der Tastatur eingeben).""",
                               choices=country_codes.contry_codes_as_tuple_list,
                               default="Griechenland", null=True, blank=True)
    date_from = models.PositiveIntegerField(help_text="Jahr des Baubeginns eingeben. Wenn nicht gesetzt, "
                                                      + "erscheint das Gebäude nicht auf der Zeitachse.",
                                            null=True, blank=True)
    date_from_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Baubeginns: v.Chr. bzw. n.Chr. auswählen.",
                                          choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.",
                                          null=True, blank=True)
    date_to = models.PositiveIntegerField(help_text="Jahr des Bauendes eingeben.", null=True, blank=True)
    date_to_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Bauendes: v.Chr. bzw. n.Chr. auswählen.",
                                        choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.",
                                        null=True, blank=True)
    era = models.ForeignKey(to=Era, on_delete=models.SET_NULL, null=True, blank=True)
    architect = models.CharField(max_length=100, help_text="Architekt des Bauwerks eingeben (max. 100 Zeichen).",
                                 null=True, blank=True)
    context = models.CharField(max_length=100,
                               help_text="""Kontext des Bauwerks eingeben (Haus, Siedlung, öfftl. Platz etc., "
                                         max. 100 Zeichen)""",
                               null=True, blank=True)
    builder = models.CharField(max_length=100, help_text="Bauherren des Bauwerks eingeben (max. 100 Zeichen).",
                               null=True, blank=True)
    construction_type = models.CharField(max_length=100, help_text="Bautyp des Bauwerks eingeben (max. 100 Zeichen).",
                                         null=True, blank=True)
    design = models.CharField(max_length=100, help_text="Bauform des Bauwerks angeben. (max. 100 Zeichen)",
                              null=True, blank=True)
    function = models.CharField(max_length=100, help_text="Funktion des Bauwerks eingeben (max. 100 Zeichen).",
                                null=True, blank=True)
    length = models.FloatField(help_text="Länge des Bauwerks eingeben (falls vorhanden, in m).", null=True, blank=True)
    width = models.FloatField(help_text="Breite des Bauwerks eingeben (falls vorhanden, in m).", null=True, blank=True)
    height = models.FloatField(help_text="Höhe des Bauwerks eingeben (falls vorhanden, in m).", null=True, blank=True)
    circumference = models.FloatField(help_text="Durchmesser des Bauwerks eingeben (falls vorhanden).",
                                      null=True, blank=True)
    area = models.FloatField(help_text="Fläche des Bauwerks eingeben (falls vorhanden, in m²).", null=True, blank=True)
    column_order = models.CharField(max_length=100, help_text="Säulenordnung des Gebäudes eingeben (max. 100 Zeichen).",
                                    null=True, blank=True)
    construction = models.CharField(max_length=100,
                                    help_text="""Konstruktion des Bauwerks eingeben (z.B. Massivbau, etc., falls 
                                    vorhanden, max. 100 Zeichen)""",
                                    null=True, blank=True)
    material = models.CharField(max_length=100, help_text="Material des Bauwerks eingeben (max. 100 Zeichen).",
                                null=True, blank=True)
    literature = models.TextField(max_length=1000, help_text="Literatur zum Gebäude angeben (max. 1000 Zeichen).",
                                  null=True, blank=True)

    def __str__(self):
        return self.name

    def get_name(self, building_id):
        """
        :return: name of the building
        """
        # pylint: disable= no-member
        building = self.objects.get(pk=building_id)
        return building.name

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

    def get_date_from_BC_or_AD(self, building_id):
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

    def get_date_to_BC_or_AD(self, building_id):
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
    name = models.CharField(max_length=100, help_text="Titel des Bauplans eingeben (max. 100 Zeichen).")
    description = models.TextField(max_length=1000, help_text="Beschreibung des Bildes eingeben (max. 1000 Zeichen).",
                                   null=True, blank=True)
    blueprint = models.ImageField(help_text="Auf \"Durchsuchen\" drücken um einen Bauplan hochzuladen.", upload_to="blueprint/",
                                width_field="width", height_field="height")
    width = models.IntegerField(editable=False, default=0)
    height = models.IntegerField(editable=False, default=0)
    building = models.ForeignKey(to=Building, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_blueprint_for_building(self, wanted_building):
        """
        Getting a list of blueprints for the given building
        :param wanted_building:
        :return: list of blueprints for given building or empty list
        """
        #pylint disable= no-member
        blueprints = self.objects.filter(building=wanted_building)
        return blueprints


class Picture(models.Model):
    name = models.CharField(max_length=100, help_text="Titel des Bildes eingeben (max. 100 Zeichen).")
    description = models.TextField(max_length=1000, help_text="Beschreibung des Bildes eingeben (max. 1000 Zeichen).",
                                   null=True, blank=True)
    picture = models.ImageField(help_text="Auf \"Durchsuchen\" drücken um ein Bild hochzuladen.", upload_to="pics/",
                                width_field="width", height_field="height")
    width = models.IntegerField(editable=False, default=0)
    height = models.IntegerField(editable=False, default=0)
    building = models.ForeignKey(to=Building, null=True, blank=True, on_delete=models.SET_NULL)
    usable_as_thumbnail = models.BooleanField(default=False,
                                              help_text="""Anwählen wenn das Bild als Thumbnail (Vorschaubild) für sein 
                                              Bauwerk in der Zeitachse und den Bauwerken erscheinen darf. Bei mehreren 
                                              möglichen Vorschaubildern für ein Bauwerk wird zufällig eins """)

    def __str__(self):
        return self.name

    def get_picture_for_building(self, wanted_building):
        """
        Getting a List of Pictures for the given building
        :param wanted_building:
        :return: list of Pictures for given building or empty list
        """
        #pylint disable= no-member
        pictures = self.objects.filter(building=wanted_building)
        return pictures

