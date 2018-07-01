from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST 
from . import models
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
        data = models.Exam.as_dict_entry()
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
        course=req['course'],
    )
    newExam.save()
    # We may assume that all questions in QuestionDetail exists
    for question in req['QuestionDetail']:
        id = int(question['id'])
        newExam.questions.add(models.Question.objects.get(id=id))
    return JsonResponse("OK")

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
        for question in exam.questions.all():
            for q in req['QuestionDetail']:
                if question.id == int(q['id']):
                    exam.questions.remove(id=question.id)
                    break
        for question in req['QuestionDetail']:
            id = int(question['id'])
            exam.questions.add(models.Question.objects.get(id=id))
        return JsonResponse("OK")

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
        exam.delte()
        return JsonResponse("OK")

#/exam/{exam-id}/participate GET
@require_GET
def participateExam(request, exam_id):
    try:
        exam = models.Exam.objects.get(pk=exam_id)
    except (KeyError, models.Exam.DoesNotExist):
        return HttpResponse("The required exam does not exist.", status=444)
    except:
        return UnexpectedErrorResponse()
    else:
        # Need to acquire the userid
        userid = 1
        startTime = timezone.now()
        participation = models.ExamParticipation(
            userid=userid,
            starttime=startTime,
            endtime=exam.availableendtime, 
            score=None,
            examid=exam_id,
            answer="",
        ) 
        participation.save()
        return exam.as_dict_paper()

#/exam/{exam-id}/submit/ POST
@require_POST
def submitExam(request, exam_id):
    submitTime = timezone.now()
    req = json.loads(request.body.decode())
    try:
        exam = models.Exam.objects.get(pk=exam_id)
    except (KeyError, models.Exam.DoesNotExist):
        return HttpResponse("The required exam does not exist.", status=444)
    except:
        return UnexpectedErrorResponse()
    else:
        if submitTime > exam.availableendtime or submitTime < exam.availablestarttime:
            return HttpResponse("The exam is not available now.", status=444) 
        else:
            # Need to acquire the userid
            userid = 1
            try:
                participation = models.ExamParticipation.get(userid=userid)
            except (KeyError, models.ExamParticipation.DoesNotExist):
                return HttpResponse("The user did not participate this exam.", status=444)
            except:
                return UnexpectedErrorResponse()
            else:
                answer = ""
                for s in req:
                    answer += s
                    answer += " \n"
                participation.answer = answer
                participation.save()
                return JsonResponse("OK")
