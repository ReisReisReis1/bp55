# Generated by Django 3.1.5 on 2021-11-04 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='content',
            field=models.CharField(help_text='Inhalt der Ankündigung.', max_length=105, verbose_name='Inhalt'),
        ),
    ]
