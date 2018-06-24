# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from OnlineExam.tools import *
import json

class Chapter(models.Model):
    name = models.CharField(max_length=255)

class Question(models.Model):
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True)
    options = models.TextField(max_length=255, blank=True)
    solution = models.CharField(max_length=20, blank=True)
    author = models.IntegerField(blank=True, null=True)
    keypoints = models.TextField(blank=True)
    def set_options(self, x):
        if not x is None:
            self.options = json.dumps(x)
        else:
            self.options = ""
    def get_options(self):
        return json.loads(self.options)
    def set_keypoints(self, x):
        if not x is None:
            self.keypoints = json.dumps(x)
        else:
            self.keypoints = ""
    def get_keypoints(self):
        return json.loads(self.keypoints)
    def as_dict_entry(self):
        d = dict()
        d['id'] = self.pk
        d['type'] = self.type
        d['description'] = self.description
        d['author'] = self.author
    def as_dict_detail(self):
        d = self.as_dict_entry()
        d['solution'] = self.solution
        d['keypoints'] = self.keypoints

class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    displaystarttime = models.DateTimeField(db_column='displayStartTime', blank=True, null=True)  # Field name made lowercase.
    displayendtime = models.DateTimeField(db_column='displayEndTime', blank=True, null=True)  # Field name made lowercase.
    availablestarttime = models.DateTimeField(db_column='availableStartTime', blank=True, null=True)  # Field name made lowercase.
    avaliableendtime = models.DateTimeField(db_column='avaliableEndTime', blank=True, null=True)  # Field name made lowercase.
    createat = models.DateTimeField(db_column='createAt', blank=True, null=True)  # Field name made lowercase.
    courseid = models.IntegerField(db_column='courseId', blank=True, null=True)  # Field name made lowercase.
    chapters = models.ManyToManyField(Chapter)
    questions = models.ManyToManyField(Question)
    def as_dict_entry(self):
        d = dict()
        d['id'] = self.id
        d['name'] = self.name
        d['description'] = self.description
        # handle enum type manually
        d['displayStartTime'] = datetime_to_js_timestamp(self.displaystarttime)
        d['displayEndTime'] = datetime_to_js_timestamp(self.displayendtime)
        d['availableStartTime'] = datetime_to_js_timestamp(self.availablestarttime)
        d['availableEndTime'] = datetime_to_js_timestamp(self.availableendtime)
        d['creatAt'] = datetime_to_js_timestamp(self.createat)
        d['course'] = self.courseid
        return d

    def as_dict_paper(self):
        d['questions'] = []
        for question in self.questions.all():
            d['questions'].append(question.as_dict_detail())

    def as_dict_detail(self):
        d = self.as_dict_paper()
        d['participation'] = []
        for participation in self.examparticipation_set.all():
            d['participation'].append(participation.as_dict())
        return d



class ExamParticipation(models.Model):
    userid = models.IntegerField(db_column='userId')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(blank=True, null=True)
    examid = models.ForeignKey(Exam, models.DO_NOTHING, db_column='examId')  # Field name made lowercase.
    answer = models.TextField(blank=True, null=True)  # This field type is a guess.
    def as_dict(self):
        d = dict()
        d['id'] = self.id
        d['user'] = self.userid
        d['startTime'] = datetime_to_js_timestamp(self.starttime)
        d['endTime'] = datetime_to_js_timestamp(self.endtime)
        d['score'] = self.score
        d['exame'] = self.examid
        d['answer'] = self.answer


class QuestionGroup(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    
