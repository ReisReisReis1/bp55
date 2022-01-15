# Generated by Django 3.1.5 on 2021-11-09 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IntroTexts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro_text', models.TextField(help_text='Allgemeiner Text für die Intro-Seite (max. 5000 Zeichen).', max_length=5000, verbose_name='Intro-Text')),
                ('timeline_card_text', models.TextField(help_text='Text für die Zeitachsen Karte (max. 200 Zeichen).', max_length=200, verbose_name='Zeitachsen Karten Text')),
                ('buildings_card_text', models.TextField(help_text='Text für die Bauwerke Karte (max. 200 Zeichen).', max_length=200, verbose_name='Bauwerke Karten Text')),
                ('video_card_text', models.TextField(help_text='Text für die Video Karte (max. 200 Zeichen).', max_length=200, verbose_name='Video Karten Text')),
            ],
        ),
    ]