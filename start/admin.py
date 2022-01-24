"""
Possibility to add sth to Admin Interface out of this APP: start
"""
from django.contrib import admin
from .models import IntroTexts

admin.site.register(IntroTexts)
