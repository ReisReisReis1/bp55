# Generated by Django 3.1.5 on 2021-03-05 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0005_auto_20210304_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicdate',
            name='year',
            field=models.PositiveIntegerField(blank=True, help_text='Hier das Jahr des Ereignisses einfügen. Falls es ein genaueres Datum gibt, wird diese angezeigt.', null=True, verbose_name='Jahr'),
        ),
    ]
