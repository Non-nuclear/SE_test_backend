# Generated by Django 2.0.6 on 2018-06-23 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('displaystarttime', models.DateTimeField(blank=True, db_column='displayStartTime', null=True)),
                ('displayendtime', models.DateTimeField(blank=True, db_column='displayEndTime', null=True)),
                ('availablestarttime', models.DateTimeField(blank=True, db_column='availableStartTime', null=True)),
                ('avaliableendtime', models.DateTimeField(blank=True, db_column='avaliableEndTime', null=True)),
                ('createat', models.DateTimeField(blank=True, db_column='createAt', null=True)),
                ('courseid', models.IntegerField(blank=True, db_column='courseId', null=True)),
                ('chapters', models.ManyToManyField(to='dao.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='ExamParticipation',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('userid', models.IntegerField(db_column='userId')),
                ('starttime', models.DateTimeField(blank=True, db_column='startTime', null=True)),
                ('endtime', models.DateTimeField(blank=True, db_column='endTime', null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('awnser', models.TextField(blank=True, null=True)),
                ('examid', models.ForeignKey(db_column='examId', on_delete=django.db.models.deletion.DO_NOTHING, to='dao.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('options', models.TextField(blank=True, max_length=255, null=True)),
                ('solution', models.CharField(blank=True, max_length=20, null=True)),
                ('author', models.IntegerField(blank=True, null=True)),
                ('keypoints', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('questions', models.ManyToManyField(to='dao.Question')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='questions',
            field=models.ManyToManyField(to='dao.Question'),
        ),
    ]
