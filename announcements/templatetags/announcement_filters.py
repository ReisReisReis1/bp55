"""
New Filters that can be used in templates
"""
from timeline.templatetags.app_filters import register
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiplies a and b.
    :param value: One int
    :param arg: Another int
    :return: value * arg
    """
    return int(value) * int(arg)
