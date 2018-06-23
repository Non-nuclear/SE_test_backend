# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import json

class Chapter(models.Model):
    name = models.CharField(max_length=255)

class Question(models.Model):
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)
    options = models.TextField(max_length=255, blank=True, null=True)
    solution = models.CharField(max_length=20, blank=True, null=True)
    author = models.IntegerField(blank=True, null=True)
    keypoints = models.TextField(blank=True, null=True)
    def set_options(self, x):
        self.options = json.dumps(x)
    def get_options(self):
        return json.loads(self.options)
    def set_keypoints(self, x):
        self.keypoints = json.dumps(x)
    def get_keypoints(self):
        return json.loads(self.keypoints)

class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    displaystarttime = models.DateTimeField(db_column='displayStartTime', blank=True, null=True)  # Field name made lowercase.
    displayendtime = models.DateTimeField(db_column='displayEndTime', blank=True, null=True)  # Field name made lowercase.
    availablestarttime = models.DateTimeField(db_column='availableStartTime', blank=True, null=True)  # Field name made lowercase.
    avaliableendtime = models.DateTimeField(db_column='avaliableEndTime', blank=True, null=True)  # Field name made lowercase.
    createat = models.DateTimeField(db_column='createAt', blank=True, null=True)  # Field name made lowercase.
    courseid = models.IntegerField(db_column='courseId', blank=True, null=True)  # Field name made lowercase.
    chapters = models.ManyToManyField(Chapter)
    questions = models.ManyToManyField(Question)



class ExamParticipation(models.Model):
    userid = models.IntegerField(db_column='userId')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(blank=True, null=True)
    examid = models.ForeignKey(Exam, models.DO_NOTHING, db_column='examId')  # Field name made lowercase.
    awnser = models.TextField(blank=True, null=True)  # This field type is a guess.




class QuestionGroup(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)

        

