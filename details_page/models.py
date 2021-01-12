"""
Configurations for the Database Models for the App 'details_page'
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import CharField, Value as V
from django.db.models.functio

class Detail(models.model):
    """
    name: name of the building
    city: city in which the building is located
    region: region in which the buildind is located
    country: country in which the building is located
    date_from: date on which construction began
    date_to: date on which construction ended
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
    videos: videos about the building
    pictures: pictures of teh building
    building_plan: building plan of the building
    """
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=5)
    date_from: models.DateField()
    date_to: models.DateField()
    architect = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    builder = models.CharField(max_length=100)
    construction_type = models.CharField(max_length=100)
    design = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    circumference = models.FloatField()
    area= models.FloatField()
    column_order = models.CharField(max_length=100)
    construction = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    literature = models.TextField()
    era = models.CharField(max_length=100,
                           choices=[
                               ('Frühzeit', 'Frühzeit'), ('Archaik', 'Archaik'),
                               ('Klassik', 'Klassik'), ('Hellenismus', 'Hellenismus'),
                               ('Römische Kaiserzeit', 'Römische Kaiserzeit'),
                               ('Spätantike', 'Spätantike'),
                               ('Sonstiges', 'Sonstiges'),
                           ], default='Sonstiges')
    videos =  models.FileField()
    pictures = models.ImageField()
    building_plan = models.ImageField()

    def get_name(self):
        """
        :return: name of the building
        """
        return self.name

    def get_city(self):
        """
        :return: city in which the building is located
        """
        return self.city

    def get_region(self):
        """
        :return: region in which the building is located
        """
        return self.region

    def get_country(self):
        """
        :return: country in which the building is located
        """
        return self.country

    def get_date(self):
        """
        :return: date
        """


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

    def get_





