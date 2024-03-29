# Generated by Django 3.1.14 on 2021-12-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details_page', '0014_auto_20211109_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='era',
            name='name',
            field=models.CharField(choices=[('Mykenische Zeit', 'Mykenische Zeit'), ('Frühe Eisenzeit', 'Frühe Eisenzeit'), ('Archaik', 'Archaik'), ('Klassik', 'Klassik'), ('Hellenismus', 'Hellenismus'), ('römische Republik', 'römische Republik'), ('Kaiserzeit', 'Kaiserzeit'), ('Spätantike', 'Spätantike'), ('Rezeption', 'Rezeption')], help_text='Epoche auswählen.', max_length=100, unique=True, verbose_name='Name'),
        ),
    ]
