# Generated by Django 3.1.5 on 2021-01-22 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('details_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(default=0, help_text='Hier das Jahr des Ereignisses einfügen.\n                                        Falls es ein genaueres Datum gibt, wird diese angezeigt. Damit es sich ist, \n                                        dass ein Datum gegeben ist, muss dieses Feld hier aber ausgefüllt werden . ')),
                ('exacter_date', models.DateField(blank=True, help_text="Falls das Ereignis ein genaueres Datum hat, hier eingeben.\n                                         Diese Feld unterstützt zusätzlich zur Jahreszahl (wie obendrüber), \n                                         Monats- und Tagesangaben, es kann aber auch leer bleiben.\n                                         Falls diese und die Jahreszahl gesetzt sind, wird dieses genauere Datum das \n                                         sein, dass angezeigt wird. ACHTUNG: Jahreszahlen bitte vierstellig eingeben: \n                                         Das Jahr '17' wird sonst automatisch zu '2017' erweitert, \n                                         möchte man das Jahr 17 haben, muss man '0017' eingeben.", null=True)),
                ('year_BC_or_AD', models.CharField(choices=[('v.Chr.', 'v.Chr.'), ('n.Chr.', 'n.Chr.')], default='v.Chr.', help_text='Jahr des Ereignisses: v.Chr. bzw. n.Chr. auswählen.', max_length=7)),
                ('title', models.CharField(help_text='Hier einen Titel für der Ereignis einfügen (max. 100 Zeichen).', max_length=100)),
                ('infos', models.TextField(help_text='Hier eine kurze Beschreibung des historischen Ereignisses einfügen (max. 1000 Zeichen).', max_length=1000)),
                ('era', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='details_page.era')),
            ],
        ),
    ]
