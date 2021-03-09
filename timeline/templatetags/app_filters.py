from django import template
from django.template.defaulttags import register

register = template.Library()


@register.filter
def key(dictionary, key):
    return [dictionary.get(key)]
