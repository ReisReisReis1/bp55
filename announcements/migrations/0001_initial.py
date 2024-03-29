# Generated by Django 3.1.5 on 2021-11-04 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False, verbose_name='Aktiv?')),
                ('title', models.CharField(choices=[('Wartungsarbeiten', 'Wartungsarbeiten'), ('Jetzt Neu', 'Jetzt Neu'), ('Erinnerung', 'Erinnerung')], help_text='Den Typ der Ankündigung auswählen.', max_length=20, verbose_name='Titel')),
                ('content', models.CharField(help_text='Inhalt der Ankündigung.', max_length=95, verbose_name='Inhalt')),
            ],
            options={
                'verbose_name': 'Ankündigung',
                'verbose_name_plural': 'Ankündigungen',
            },
        ),
    ]
