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


@register.filter
def calc_font_size(s, is_mobile=False):
    """
    Used to calculate font sizes from string length for timeline years.

    :param s: The string for which the font size should be calculated.
    :param is_mobile: If it will be used in mobile design or not.
    """
    if s == "":
        # no building year is given, return default font sizes (for "N/A")
        if not is_mobile:
            return 24
        else:
            return 12  # on mobile just "N/A" can be bigger then the default size
    if not is_mobile:
        # as long as a limit of 15 is not exceeded, it will get the standard font size
        if len(s) >= 15:
            # else this function will modell the font size: f(x) = -0.6*(x-16)²+24
            # with 16 and 24 for the limit and the standard (that the crossing point after standard
            # will match with the function).
            # and 0.6 is a factor for speed of decreasing
            f = -0.8*math.pow(len(s)-16, 2)+24
            # for float results: replace "," with "." for css to recognize it as a floating number
            return str(f).replace(",", ".")
        return 24  # default font size
    else:
        if len(s) >= 11:
            # a optimized version of the function from above for the mobile design
            f = -0.09*math.pow(len(s)-12, 2)+11
            return str(f).replace(",", ".")
        return 11  # default font size
