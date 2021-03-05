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

    :param dictionary: Dictionary from which index element gets returned
    :param index: Index of desired element
    :return: Dictionary element which is stored under given key/index
    """
    return [dictionary.get(index)]

@register.filter
def index(list, i):
    """
    Returns the Element of a list on index i

    :param list: List from which index element gets returned
    :param i: Index of desired element
    :return: Element of list on index i
    """
    return list[i]