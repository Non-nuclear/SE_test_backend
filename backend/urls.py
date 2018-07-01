from django.urls import path
from . import views

app_name = "backend"
urlpatterns =[
    path('account/profile/', views.getUser),
    path('account/fake-login/', views.fake_login),

    path('question/<int:questionid>/', views.getQuestion),
    path('question/create/', views.createQuestion),
    path('question/list/', views.getQuestionList),
    path('question/<int:questionid>/update/', views.updateQuestion),
    path('question/<int:questionid>/delete/', views.deleteQuestion),
    
    path('question/group/list/', views.getQuestionGroupList),
    path('question/group/<int:questiongroupid>/', views.getQuestionGroup),
    path('question/group/create/', views.createQuestionGroup),
    path('question/group/<int:questiongroupid>/update/', views.updateQuestionGroup),
    path('question/group/<int:questiongroupid>/delete/', views.deleteQuestionGroup),

    path('exam/list/', views.getExamList),
    path('exam/<int:exam_id>/', views.getExam),
    path('exam/create/', views.createExam),
    path('exam/<int:exam_id>/update/', views.updateExam),
    path('exam/<int:exam_id>/delete/', views.deleteExam),
    path('exam/<int:exam_id>/participate/', views.participateExam),
    path('exam/<int:exam_id>/submit/', views.submitExam),
]


