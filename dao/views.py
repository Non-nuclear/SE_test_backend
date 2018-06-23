from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from . import models
import json
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

#/question/list/ GET
def getQuestionList(request):
    qset = models.Question.objects.all()
    qlist = []
    for q in qset:
        data = {
            'id' : q.id,
            'type': q.type,
            'description' :q.description,
            'author' : q.author
        }
        qlist.append(data)
    j = json.dumps(qlist, cls=DjangoJSONEncoder)
    return HttpResponse(j)

#/question/{question-id}/ GET
def getQuestion(request, questionid):
    q = models.Question.objects.get(id=questionid)
    data = {
        'options' : q.get_options(), 
        'solution' : q.solution, 
        'keypoints' : q.get_keypoints()
    }
    return JsonResponse(data)

#/question/create/ POST
def createQuestion(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        m = models.Question(
            type = req['type'],
            description = req['description'],
            solution = req['solution']
            )
        m.set_options(req['options'])
        m.set_keypoints(req['keypoints'])
        m.save()
        return HttpResponse(m.id)

   
#/question/{question-id}/update/ POST
def updateQuestion(request, questionid):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        q = models.Question.objects.get(id=questionid)
        q.type = req['type']
        q.description = req['description']
        q.solution = req['solution']
        q.set_options(req['options'])
        q.set_keypoints(req['keypoints'])
        q.save()
        return HttpResponse("OK")

#/question/{question-id}/delete/ GET
def deleteQuestion(request, questionid):
    models.Question.objects.filter(id=questionid).delete()
    return HttpResponse("OK")



######
######


#/question/group/list/ GET
def getQuestionGroupList(request):
    qgset = models.QuestionGroup.objects.all()
    qglist = []
    for qg in qgset:
        data = {
            'id' : qg.id,
            'name': qg.name
        }
        qglist.append(data)
    j = json.dumps(qglist, cls=DjangoJSONEncoder)
    return HttpResponse(j)

#/question/group/{question-group-id}/ GET
def getQuestionGroup(request, questiongroupid):
    qg = models.QuestionGroup.objects.get(id=questiongroupid)
    qgd = []
    data = {
        'id' : qg.id, 
        'name' : qg.name
    }
    qgd.append(data)
    qset = qg.questions.all()
    for q in qset:
        data = {
            "id" : q.id,
            "type" : q.type,
            "description" : q.description,
            "author" : q.author
        }
        qgd.append(data)
    j = json.dumps(qgd, cls=DjangoJSONEncoder)
    return JsonResponse(data)

#/question/group/create/ POST
def createQuestionGroup(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        qg = models.QuestionGroup(
            name = req['name']
        )
        qg.save()
        return HttpResponse(qg.id)

#/question/group/{question-group-id}/update/ POST
def updateQuestionGroup(request, questiongroupid):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        qg = models.QuestionGroup.objects.get(id=questiongroupid)
        qg.name = req['name']
        qg.save()
        return HttpResponse("OK")

#/question/group/{question-group-id}/delete/ GET
def deleteQuestionGroup(request, questiongroupid):
    models.QuestionGroup.objects.filter(id=questiongroupid).delete()
    return HttpResponse("OK")

