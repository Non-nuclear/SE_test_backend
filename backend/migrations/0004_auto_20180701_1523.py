# Generated by Django 2.0.6 on 2018-07-01 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20180701_1521'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='avaliableendtime',
            new_name='availableendtime',
        ),
    ]
