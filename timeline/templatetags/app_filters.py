"""
New Filters that can be used in templates
"""
import math

from django import template
from django.template.defaulttags import register

register = template.Library()


@register.filter
def index(lst, i):
    """
    Returns the Element of a list on index i

    :param lst: List from which index element gets returned
    :param i: Index of desired element
    :return: Element of list on index i
    """
    return lst[i]
