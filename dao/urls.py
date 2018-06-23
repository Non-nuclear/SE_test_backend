from django.urls import path
from . import views

urlpatterns =[
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
]


