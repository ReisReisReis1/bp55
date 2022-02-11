from .models import Announcement


# Create your views here.
def get_announcements():
    w_announcements = Announcement.objects.filter(active=True, title="Wartungsarbeiten")
    announcements = Announcement.objects.filter(active=True).exclude(title="Wartungsarbeiten")
    context = {}
    animation_duration_scalar = 10
    if w_announcements:
        # the animation speed depends on the string length.
        # calculate and make reasonable second amount of it
        str_len = 5*len("+++        ")+5*len(": ")
        for a in w_announcements:
            str_len += 5*(len(a.title)+len(a.content))
        seconds = str(str_len/animation_duration_scalar)
        seconds = seconds.replace(",", ".")
        context[(True, seconds)] = [w_announcements for i in range(5)]
    if announcements:
        str_len = 5 * len("+++        ") + 5 * len(": ")
        for a in announcements:
            str_len += 5 * (len(a.title) + len(a.content))
        seconds = str(str_len/animation_duration_scalar)
        seconds = seconds.replace(",", ".")
        context[(False, seconds)] = [announcements for i in range(5)]
    return context
