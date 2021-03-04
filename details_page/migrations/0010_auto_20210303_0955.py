# Generated by Django 3.1.5 on 2021-03-03 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details_page', '0009_auto_20210217_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='date_century',
            new_name='year_century',
        ),
        migrations.RenameField(
            model_name='building',
            old_name='date_from',
            new_name='year_from',
        ),
        migrations.RenameField(
            model_name='building',
            old_name='date_from_BC_or_AD',
            new_name='year_from_BC_or_AD',
        ),
        migrations.RenameField(
            model_name='building',
            old_name='date_to',
            new_name='year_to',
        ),
        migrations.RenameField(
            model_name='building',
            old_name='date_to_BC_or_AD',
            new_name='year_to_BC_or_AD',
        ),
        migrations.RemoveField(
            model_name='building',
            name='date_ca',
        ),
        migrations.AddField(
            model_name='building',
            name='year_ca',
            field=models.BooleanField(default=False, help_text='ca. zum Datum hinzufügen (für ungenaue Datumsangaben).', verbose_name='ungefähre Jahresangabe?'),
        ),
        migrations.AlterField(
            model_name='era',
            name='name',
            field=models.CharField(choices=[('Bronzezeit', 'Bronzezeit'), ('Frühzeit', 'Frühzeit'), ('Archaik', 'Archaik'), ('Klassik', 'Klassik'), ('Hellenismus', 'Hellenismus'), ('Kaiserzeit', 'Kaiserzeit'), ('Spätantike', 'Spätantike'), ('Sonstiges', 'Sonstiges')], help_text='Epoche auswählen.', max_length=100, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='era',
            name='year_to_BC_or_AD',
            field=models.CharField(blank=True, choices=[('v.Chr.', 'v.Chr.'), ('n.Chr.', 'n.Chr.')], default='v.Chr.', help_text='Jahr des Endes: v.Chr. bzw. n.Chr. auswählen.', max_length=7, null=True, verbose_name='Enddatum v.Chr/n.Chr.?'),
        ),
    ]
