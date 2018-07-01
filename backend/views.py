from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST 
from . import models
from .models import Question,QuestionGroup
from OnlineExam.tools import *
import json
from django.core.serializers.json import DjangoJSONEncoder

user = {
    'id' : '0',
    'name' : 'test',
    'type' : 'student'
}

###account
def getUser(request):
    return JsonResponse(user)

def fake_login(request):
    req = json.loads(request.body.decode())
    if request.method == 'POST':
        global user
        user = req
        return HttpResponse("OK")
        
        

# Create your views here.
def UnexpectedErrorResponse():
    return HttpResponse("Unexpected Error!", status=500)

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
    return JsonResponse(qlist, safe=False)

#/question/{question-id}/ GET
def getQuestion(request, questionid):
    q = models.Question.objects.get(id=questionid)
    data = {
        'id' : q.id,
        'type': q.type,
        'description' : q.description,
        'author' : q.author,
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
            solution = req['solution'],
            author = user['name']
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
    return JsonResponse(qglist, safe=False)

#/question/group/{question-group-id}/ GET
def getQuestionGroup(request, questiongroupid):
    qg = models.QuestionGroup.objects.get(id=questiongroupid)
    questions = []
    data = {
        'id' : qg.id, 
        'name' : qg.name
    }
    for q in qg.questions.all():
        questions.append(q.as_dict_entry())
    # j = json.dumps(qgd, cls=DjangoJSONEncoder)
    data['questions'] = questions
    return JsonResponse(data)

#/question/group/create/ POST
def createQuestionGroup(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode())
        qg = models.QuestionGroup(
            name = req['name']
        )
        qg.save()
        for id in req['questionIds']:
            question = Question.objects.get(id=id)
            qg.questions.add(question)
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
###########################

#/exam/list/ GET
def getExamList(request):
    exset = models.Exam.objects.all()
    exlist = []
    for ex in exset:
        data = ex.as_dict_detail()
        data['participated'] = ex.participations.filter(userid=user['id']).exists()
        if data['participated']:
            p = ex.participations.filter(userid=user['id'])[0]
            if p.endtime is not None:
                data['score'] = p.score
            else:
                data['score'] = '进行中'
        exlist.append(data)
    return JsonResponse(exlist, safe=False)

#/exam/{exam-id}/ GET
# require teacher permission
@require_GET
def getExam(request, exam_id):
    try:
        exam = models.Exam.objects.get(pk=exam_id)
    except (KeyError, models.Exam.DoesNotExist):
        return HttpResponse("The required exam does not exist.", status=444)
    except:
        return UnexpectedErrorResponse()
    else:
        return JsonResponse(exam.as_dict_detail())


#/exam/create/ POST
# require teacher permission
@require_POST
def createExam(request):
    req = json.loads(request.body.decode())
    if req['description'] is None:
        req['description'] = ""
    newExam = models.Exam(
        name=req['name'],
        description=req['description'],
        displaystarttime=req['displayStartTime'],
        displayendtime=req['displayEndTime'],
        availablestarttime=req['availableStartTime'],
        availableendtime=req['availableEndTime'],
        # course=req['course'],
    )
    newExam.save()
    # We may assume that all questions in QuestionDetail exists
    for id in req['questionIds']:
        newExam.questions.add(models.Question.objects.get(id=id))
    return HttpResponse()

#/exam/{exam-id}/update POST
# require teacher permission
@require_POST
def updateExam(request, exam_id):
    try:
        exam = models.Exam.objects.get(pk=exam_id)
    except (KeyError, models.Exam.DoesNotExist):
        return HttpResponse("The required exam does not exist.", status=444)
    except:
        return UnexpectedErrorResponse()
    else:
        req = json.loads(request.body.decode())
        if req['description'] is None:
            req['description'] = ""
        exam.name = req['name']
        exam.description = req['description']
        exam.displaystarttime = req['displayStartTime']
        exam.displayendtime = req['displayEndTime']
        exam.availablestarttime = req['availableStartTime']
        exam.availableendtime = req['availableEndTime']
        exam.course = req['course']
        exam.save()
        exam.questions.clear()
        for id in req['questionIds']:
            exam.questions.add(models.Question.objects.get(id=id))
        return HttpResponse()

#/exam/{exam-id}/delete GET
# require teacher permission
@require_GET
def deleteExam(request, exam_id):
    try:
        exam = models.Exam.objects.get(pk=exam_id)
    except (KeyError, models.Exam.DoesNotExist):
        return HttpResponse("The required exam does not exist.", status=444)
    except:
        return UnexpectedErrorResponse()
    else:
        exam.delete()
        return HttpResponse()

#/exam/{exam-id}/participate GET
@require_GET
def participateExam(request, exam_id):
    try:
        exam = models.Exam.objects.get(pk=exam_id)
    except (KeyError, models.Exam.DoesNotExist):
        return UnexpectedErrorResponse()
        # return HttpResponse("The required exam does not exist.", status=444)
    # except:
        # return UnexpectedErrorResponse()
    # Need to acquire the userid
    userid = user['id']
    startTime = timezone.now()
    if not models.ExamParticipation.objects.filter(userid=userid,exam=exam).exists():
        participation = models.ExamParticipation(
            userid=userid,
            starttime=startTime,
            endtime=None,
            score=None,
            exam=exam,
            answer="",
        )
        participation.save()
    return JsonResponse(exam.as_dict_paper())

#/exam/{exam-id}/submit/ POST
@require_POST
def submitExam(request, exam_id):
    submitTime = timezone.now()
    req = json.loads(request.body.decode())
    try:
        exam = models.Exam.objects.get(id=exam_id)
    except (KeyError, models.Exam.DoesNotExist):
        return HttpResponse("The required exam does not exist.")
    except:
        return UnexpectedErrorResponse()
    if submitTime > exam.availableendtime or submitTime < exam.availablestarttime:
        return HttpResponse("The exam is not available now.") 
    userid = user['id']
    try:
        participation = exam.participations.get(userid=userid)
    except (KeyError, models.ExamParticipation.DoesNotExist):
        return HttpResponse("The user did not participate this exam.")
    except:
        return UnexpectedErrorResponse()
    participation.answer = json.dumps(req)
    participation.endtime = submitTime
    score = 0
    count = 0
    questions = exam.questions.all()
    for choice in req:
        if questions[count].solution == choice:
            score+=1
        count+=1
    participation.score = score
    participation.save()
    return HttpResponse("success")


@require_GET
def examResult(request, exam_id):
    exam = models.Exam.objects.get(id=exam_id)
    res = []
    for p in exam.participations.all():
        if p.endtime is not None:
            res.append(p.as_dict())
    return JsonResponse(res, safe=False)

