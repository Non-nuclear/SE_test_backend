# Generated by Django 2.0.6 on 2018-07-01 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20180701_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='createat',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
