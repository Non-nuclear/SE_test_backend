# Generated by Django 2.0.6 on 2018-07-01 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20180701_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='chapters',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='courseid',
        ),
    ]
