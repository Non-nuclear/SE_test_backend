from  dao.models import *
from django.http import HttpResponse

def getQuestionById(id):
    # 初始化
    response = ""
    
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    alist = Question.objects.all()

    # 输出所有数据
    for var in alist:
        response += var.description + " "
    return HttpResponse("<p>" + response + "</p>")
