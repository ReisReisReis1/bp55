# Generated by Django 3.1.14 on 2022-02-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0003_auto_20220202_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='introtexts',
            name='buildings_card_text',
            field=models.TextField(help_text='Text für die Bauwerke Karte (max. 250 Zeichen).', max_length=250, verbose_name='Bauwerke Karten Text'),
        ),
        migrations.AlterField(
            model_name='introtexts',
            name='timeline_card_text',
            field=models.TextField(help_text='Text für die Zeitachsen Karte (max. 250 Zeichen).', max_length=250, verbose_name='Zeitachsen Karten Text'),
        ),
        migrations.AlterField(
            model_name='introtexts',
            name='video_card_text',
            field=models.TextField(help_text='Text für die Video Karte (max. 250 Zeichen).', max_length=250, verbose_name='Video Karten Text'),
        ),
    ]
