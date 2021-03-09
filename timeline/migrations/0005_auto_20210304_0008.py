# Generated by Django 3.1.5 on 2021-03-03 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0004_auto_20210216_1433'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicdate',
            old_name='date_ca',
            new_name='year_ca',
        ),
        migrations.RenameField(
            model_name='historicdate',
            old_name='date_century',
            new_name='year_century',
        ),
        migrations.AlterField(
            model_name='historicdate',
            name='year',
            field=models.PositiveIntegerField(default=9999, help_text='Hier das Jahr des Ereignisses einfügen. Falls es ein genaueres Datum gibt, wird diese angezeigt.', verbose_name='Jahr'),
        ),
        migrations.AlterField(
            model_name='historicdate',
            name='year_BC_or_AD',
            field=models.CharField(choices=[('v.Chr.', 'v.Chr.'), ('n.Chr.', 'n.Chr.')], default='n.Chr.', help_text='Jahr des Ereignisses: v.Chr. bzw. n.Chr. auswählen.', max_length=7, verbose_name='vor oder nach Christigeburt?'),
        ),
    ]