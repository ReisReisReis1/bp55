# Generated by Django 3.1.5 on 2021-02-17 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details_page', '0007_auto_20210216_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='links',
            field=models.TextField(blank=True, help_text='Weiterführende Links zum Gebäude angeben (max. 1000 Zeichen).', max_length=1000, null=True, verbose_name='Links'),
        ),
    ]
