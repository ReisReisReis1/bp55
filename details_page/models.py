"""
Configurations for the Database Models for the App 'details_page'
"""

from django.db import models
from . import country_codes


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
    ], default='Sonstiges',
                            help_text="Epoche auswählen")
    year_from = models.PositiveIntegerField(help_text="Jahr des Beginns der Epoche eingeben.", blank=True, null=True)
                                            #label="Jahr des Beginns der Epoche:")
    year_from_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Beginns: v.Chr. bzw. n.Chr. auswählen.",
                                          choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.",
                                          null=True, blank=True)
                                          #label="Ist das Jahr des Beginns der Epoche vor oder nach Christus?:")
    year_to = models.PositiveIntegerField(help_text="Jahr des Endes der Epoche eingeben.", blank=True, null=True)
                                          #label="Jahr des Endes der Epoche:")
    year_to_BC_Or_AD = models.CharField(max_length=7, help_text="Jahr des Endes: v.Chr. bzw. n.Chr. auswählen.",
                                        choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.",
                                        null=True, blank=True)
                                        #label="Ist das Jahr des Endes der Epoche vor oder nach Christus?:")

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
    circumference: circumference of the building ( for circular buildings9
    area: surface area of the building
    column_order: column order of the building
    construction: construction of the building
    material: material of the building
    literature: further literature about the building
    era: era in which the building was built
    #videos: videos about the building
    #pictures: pictures of teh building
    #building_plan: building plan of the building
    """

    # Added help_texts everywhere
    name = models.CharField(max_length=100, help_text="Namen des Bauwerks eingeben (max. 100 Zeichen).")
    city = models.CharField(max_length=100, help_text="Stadt des Bauweks eingeben (max. 100 Zeichen).",
                            null=True, blank=True)
    region = models.CharField(max_length=100, help_text="Region des Bauwerks eingeben (max. 100 Zeichen).",
                              null=True, blank=True)
    country = models.CharField(max_length=100, help_text="""Hier Land des Bauwerks auswählen (Tipp: Zum Suchen Kürzel 
                               auf der Tastatur eingeben).""",
                               # Country code choices in different file (for better readable code here)
                               choices=country_codes.contry_codes_as_tuple_list,
                               default="Griechenland", null=True, blank=True)
    # IntegerField -> Positive Integer Field, and added BC/AD choice for it
    date_from = models.PositiveIntegerField(help_text="Jahr des Baubeginns eingeben.", null=True, blank=True)
    date_from_BC_or_AD = models.CharField(max_length=7, help_text="Jahr des Baubeginns: v.Chr. bzw. n.Chr. auswählen.",
                                          choices=[("v.Chr.", "v.Chr."), ("n.Chr.", "n.Chr.")], default="v.Chr.",
                                          null=True, blank=True)
    # IntegerField -> Positive Integer Field, and added BC/AD choice for it
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
    # Added max_lenght
    literature = models.TextField(max_length=1000, help_text="Literatur zum Gebäude angeben (max. 1000 Zeichen).",
                                  null=True, blank=True)

    # Added
    def __str__(self):
        return self.name


class Picture(models.Model):
    name = models.CharField(max_length=100, help_text="Titel des Bildes eingeben (max. 100 Zeichen).")
    description = models.TextField(max_length=1000, help_text="Beschreibung des Bildes eingeben (max. 1000 Zeichen).")
    picture = models.FileField(help_text="Auf \"Durchsuchen\" drücken um ein Bild hochzuladen.", upload_to="pics/")
    building = models.ForeignKey(to=Building, null=True, blank=True, on_delete=models.SET_NULL)
    usable_as_thumbnail = models.BooleanField(default=False,
                                              help_text="""Anwählen wenn das Bild als Thumbnail (Vorschaubild) für sein 
                                              Bauwerk in der Zeitachse und den Bauwerken erscheinen darf. Bei mehreren 
                                              möglichen Vorschaubildern für ein Bauwerk wird zufällig eins 
                                              ausgewählt.""")

    def __str__(self):
        return self.name

    def get_name(self):
        """
        :return: name of the building
        """
        return self.name

    def get_city_region(self):
        """
        :return: city in which the building is located
        """
        city_variable= self.city
        region_variable= self.region
        city_and_region= Concat('city' , V('/'), 'region')
        return self.city

    def get_country(self):
        """
        :return: country in which the building is located
        """
        return self.country

    def get_date(self):
        """
        :return: date
        """
        date_to_string= srting(self.date_to)
        date_from_string=string(self.date_from)
        if self.date_to<0:
            date_to_with_BCAD=Concat('date_to_string', V('BC'))
        else:
            date_to_with_BCAD=Concat('date_to_string', V('AD'))
        if self.date_from<0:
            date_from_with_BCAD=Concat('date_from_string', V('BC'))
        else:
            date_from_with_BCAD=Concat('date_from_string', V('AD'))
        date_total=Concat('date_from_with_BCAD', V('-'), 'date_to_with_BCAD')
        return date_total

    def get_architect(self):
        """
        :return: architect of the building
        """
        return self.architect

    def get_context(self):
        """
        :return: context/type of the building
        """
        return self.context

    def get_builder(self):
        """
        :return: builder of the building
        """
        return self.builder

    def get_construction_type(self):
        """
        :return: construction type of the building
        """
        return self.construction

    def get_design(self):
        """
        :return: design/shape of the building
        """
        return self.design

    def get_funtion(self):
        """
        :return: function of the building
        """
        return self.function

    def get_dimension(self):
        """
        :return: Dimension of the building including length, width, height, circumference and area
        """
        length_var=self.length
        width_var=self.width
        height_var=self.height
        circumference_var=self.circumference
        area_var=self.area
        dimension= Concat(V('Länge:'), 'length_var', V('Breite:'), 'width_var', V('Höhe:'), 'height_var', V('Durchmesser'), 'circumference_var', V('Fläche:'), 'area_var')
        return dimension

    def get_column_order(self):
        """
        :return: column order of the building
        """
        return self.column_order

    def get_construction(self):
        """
        :return: construction of the building
        """
        return self.construction

    def get_material(self):
        """
        :return: material of the building
        """
        return self.material

    def get_literature(self):
        """
        :return: further literature about the building
        """
        return self.literature

    def get_videos(self):
        """
        :return: videos about the building
        """
        return self.videos

    def get_pictures(self):
        """
        :return: pictures of the building
        """
        return self.pictures

    def get_building_plan(self):
        """
        :return: building plan of the building
        """
        return self.building_plan


