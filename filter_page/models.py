"""
Configurations for the Database Models for the App 'home'
"""
"""
from django.db import models
from details_page.models import Building


class Filter(models.Model):
   
    city = models.CharField(choices=[Building.city])
    region = models.CharField(choices=[Building.region])
    country = models.CharField(choices=[Building.country])
    era = models.CharField(choices=[Building.era])
    architect = models.CharField(choices=[Building.architect])
    builder = models.CharField(choices=[Building.builder])
    design = models.CharField(choices=[Building.design])
    column_order = models.CharField(choices=[Building.column_order])

    def filter_fnc (self, criteria, ):
        
        result = list()
        
        return result
"""