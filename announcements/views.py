from .models import Announcement


# Create your views here.
def get_announcements():
    announcements = Announcement.objects.filter(active=True)
    return announcements
