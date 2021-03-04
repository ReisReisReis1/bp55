"""
New Filters that can be used in templates
"""

from django import template
from django.template.defaulttags import register

register = template.Library()


@register.filter
def key(dictionary, index):
    """
    Returns the dictionary element which is stored under the given key/index
    """
    return [dictionary.get(index)]
