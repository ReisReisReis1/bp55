# Generated by Django 3.1.5 on 2021-02-16 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_content', '0005_auto_20210216_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='length',
        ),
    ]
