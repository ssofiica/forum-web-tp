from django.shortcuts import render
from django.core.paginator import Paginator

QUEST_NUMBER = 20
ANSWER_NUMBER = 5

def pagination(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def questions(request):
    questions = []
    for i in range(1,45):
        questions.append({'title': 'Title ' + str(i),
        'id': i, 'text': 'text ' + str(i)
    })
    page_obj = pagination(questions, request, QUEST_NUMBER)
    return render(request, 'index.html', {'data': {'quest': questions, 'page_obj': page_obj}})

def hot(request):
    return render(request, '')

def tag(request):
    return render(request, '')

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    user = {'login': 'user-login', 'email': 'user@mail.ru', 'nickname': 'Mr. User'}
    return render(request, 'settings.html', {'data': user})

def question(request, id):
    q = {'title': 'Title ' + str(id),
        'id': id, 'text': 'text ' + str(id)
    }
    a = []
    for i in range(1, 10):
        a.append({'text': 'text' + str(i)})
    page_obj = pagination(a, request, ANSWER_NUMBER)
    return render(request, 'question.html', {'data': {'quest': q, 'answers': a, 'page_obj': page_obj}})