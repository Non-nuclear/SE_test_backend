# Generated by Django 2.0.6 on 2018-07-01 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20180701_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examparticipation',
            name='examid',
        ),
        migrations.AddField(
            model_name='examparticipation',
            name='exam',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='backend.Exam'),
            preserve_default=False,
        ),
    ]