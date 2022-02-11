from django.db import models


# Create your models here.
class Announcement(models.Model):
    """
    Announcement for the website.
    title: The title.
    content: The content.
    active: Whether it is active or not.
    """
    active = models.BooleanField(verbose_name="Aktiv?", default=False)
    title = models.CharField(verbose_name="Titel", max_length=30,
                             choices=[
                                 ("Wartungsarbeiten", "Wartungsarbeiten"),
                                 ("Jetzt Neu", "Jetzt Neu"),
                                 ("Neues Vorlesungsvideo", "Neues Vorlesungsvideo"),
                                 ("Klausur", "Klausur"),
                                 ("Erinnerung", "Erinnerung"),
                             ], help_text="Den Typ der Ankündigung auswählen.")
    content = models.CharField(verbose_name="Inhalt", max_length=105,
                               help_text="Inhalt der Ankündigung (max. 105 Zeichen).")

    class Meta:
        """
        Set names to show up in the admin interface.
        """
        verbose_name = "Ankündigung"
        verbose_name_plural = "Ankündigungen"

    def __str__(self):
        return self.title+": "+self.content[:50]+"..."
