from django.urls import path
from . import views

app_name = "backend"
urlpatterns =[
    path('question/<int:questionid>/', views.getQuestion),
    path('question/create/', views.createQuestion),
    path('question/list/', views.getQuestionList),
    path('question/<int:questionid>/update/', views.updateQuestion),
    path('question/<int:questionid>/delete/', views.deleteQuestion),

    path('exam/<int:exam_id>/', views.getExam),
    path('exam/create/', views.createExam),
    path('exam/<int:exam_id>/update/', views.updateExam),
    path('exam/<int:exam_id>/delete/', views.deleteExam),
    path('exam/<int:exam_id>/participate/', views.participateExam),
    path('exam/<int:exam_id>/submit/', views.submitExam),
]


