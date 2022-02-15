import math

from .models import Announcement

"""
How this works: 
The function below is imported and included in every context of every page they should be 
visible on. 
You can change announcements in the admin interface.
They are animated with marquee. This needs further explanation: 
First the html setup: In the marquee tag there are groups of spans. In each group are more 
spans, which each hold a single announcement. In every marquee there are three of these groups.
On the first group (item-collection-1 class), the swap animation is added (@keyframes swap ... in
the css file). The swap animation is there to fill up the gap between the end of the marquee, 
and the begin of the next, by translating the item collection 1 to the end. So, first the item group
1 rolls out of the screen, when 50% is passed, it is translated to the back (0% -> 100%).
If the item-collection-1's end, than closes perfectly up to the next marquee run.
To this to work without errors, the strings in each collection have to take up the whole screen.
Therefor, the inner spans with each single announcements, are duplicated till min_collection_size
is exeeded. In the code, you can also set the group_count, but 3 should be fine in any case.
Better do not set min_collection_size any lower. animation_duration_scalar is to control the
speed of the scrolling: In css you can set the animation duration in s, but most likely the
texts in warnings and normal announcements are not the same length. Which results in different
scrolling speeds from longer/shorter texts, to be scrolled completely in the same time.
To avoid this (looks ugly), we need to set the animation_duration (inline css in the html file)
variable, depending on the string length. So, if we would set string length directly there, it
would be 1 char per second. Therefore we divide the string length by this scalar. If you want
to have more speed, set a higher number, if you want lower speed, set a lower number (10 seems to
be a good choice).
The two banners (warning and normal), are placed (css position absolut) variable, depending on
which are activated. If you close one the JS script closeBanner(id) function gets called. It will
hide the banner you want to close, and set every other banner 50px up. This uses JS sessionStorage
to make sure you have to close the banners only one time per session. The function 
autoCloseSessionClosedBanners will called at page load, to make sure closed banners won't show up.
"""


def get_announcements():
    """
    Kind of the "view"-function for the announcements.
    """
    w_announcements = list(Announcement.objects.filter(active=True, title="Wartungsarbeiten"))
    announcements = list(Announcement.objects.filter(active=True).exclude(title="Wartungsarbeiten"))
    context = {}
    animation_duration_scalar = 10
    group_count = 3
    min_collection_size = 200
    constlen = len("        +++        ") + len(": ")
    if w_announcements:
        # the animation speed depends on the string length.
        # calculate and make reasonable second amount of it
        str_len = 0
        short_ws = w_announcements
        for a in w_announcements:
            str_len += (len(a.title) + len(a.content) + constlen)
        onetime_strlen = str_len
        while str_len < min_collection_size:
            str_len = str_len + onetime_strlen
            w_announcements = w_announcements + short_ws
        str_len = group_count * str_len
        seconds = str(str_len / animation_duration_scalar)
        seconds = seconds.replace(",", ".")
        context[(True, seconds)] = [w_announcements for i in range(group_count)]
    if announcements:
        str_len = 0
        short_ancmt = announcements
        for a in announcements:
            str_len = str_len + (len(a.title) + len(a.content) + constlen)
        onetime_strlen = str_len
        while str_len < min_collection_size:
            str_len = str_len + onetime_strlen
            announcements = announcements + short_ancmt
        str_len = group_count * str_len
        seconds = str(str_len / animation_duration_scalar)
        seconds = seconds.replace(",", ".")
        context[(False, seconds)] = [announcements for i in range(group_count)]
    return context
