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
    options = models.TextField(blank=True)
    solution = models.CharField(max_length=20, blank=True)
    author = models.CharField(max_length=100)
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
        return d
    def as_dict_detail(self):
        d = self.as_dict_entry()
        d['solution'] = self.solution
        d['keypoints'] = self.keypoints
        return d

class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    displaystarttime = models.DateTimeField(db_column='displayStartTime', blank=True, null=True)  # Field name made lowercase.
    displayendtime = models.DateTimeField(db_column='displayEndTime', blank=True, null=True)  # Field name made lowercase.
    availablestarttime = models.DateTimeField(db_column='availableStartTime', blank=True, null=True)  # Field name made lowercase.
    availableendtime = models.DateTimeField(db_column='avaliableEndTime', blank=True, null=True)  # Field name made lowercase.
    createat = models.DateTimeField(auto_now_add=True)  # Field name made lowercase.
    # courseid = models.IntegerField(db_column='courseId', blank=True, null=True)  # Field name made lowercase.
    questions = models.ManyToManyField(Question)
    def as_dict_entry(self):
        d = dict()
        d['id'] = self.id
        d['name'] = self.name
        d['description'] = self.description
        # handle enum type manually
        d['displayStartTime'] = self.displaystarttime.timestamp()*1000
        d['displayEndTime'] = self.displayendtime.timestamp()*1000
        d['availableStartTime'] = self.availablestarttime.timestamp()*1000
        d['availableEndTime'] = self.availableendtime.timestamp()*1000
        d['creatAt'] = self.createat.timestamp()*1000
        # d['course'] = self.courseid
        return d

    def as_dict_paper(self):
        d = self.as_dict_entry()
        d['questions'] = []
        for question in self.questions.all():
            t = question.as_dict_entry()
            t['options'] = question.get_options()
            d['questions'].append(t)
        return d

    def as_dict_detail(self):
        d = self.as_dict_entry()
        d['questions'] = []
        for question in self.questions.all():
            t = question.as_dict_detail()
            d['questions'].append(t)
        # d['participation'] = []
        # for participation in self.examparticipation_set.all():
            # d['participation'].append(participation.as_dict())
        return d



class ExamParticipation(models.Model):
    userid = models.IntegerField(db_column='userId')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(blank=True, null=True)
    exam = models.ForeignKey(Exam, models.CASCADE, related_name='participations')  # Field name made lowercase.
    answer = models.TextField(blank=True, null=True)  # This field type is a guess.
    def as_dict(self):
        d = dict()
        d['id'] = self.id
        d['user'] = self.userid
        d['startTime'] = self.starttime.timestamp()*1000
        d['endTime'] = self.endtime.timestamp()*1000
        d['score'] = self.score
        d['answer'] = json.loads(self.answer)
        return d


class QuestionGroup(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    
