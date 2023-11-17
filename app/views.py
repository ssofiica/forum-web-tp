from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Tag, Answer

QUEST_NUMBER = 20
ANSWER_NUMBER = 30

def pagination(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def questions(request):
    questions = Question.manager.get_new()
    if questions == None:
        return HttpResponse(f"Нет такой страницы")
    page_obj = pagination(questions, request, QUEST_NUMBER)
    top_tags = Tag.manager.get_top()
    data = {
        'title': 'New questions',
        'top_tags': top_tags,
        'quest': questions,
        'page_obj': page_obj,
    }
    return render(request, 'index.html', {'data': data})

def hot(request):
    questions = Question.manager.get_hot()
    if questions == None:
        return HttpResponse(f"Нет такой страницы")
    page_obj = pagination(questions, request, QUEST_NUMBER)
    return render(request, 'index.html', {'data': {'title': 'HOT questions','quest': questions, 'page_obj': page_obj}})

def tag(request, tag_name):
    tag = Tag.manager.get(name = tag_name)
    questions = Question.manager.get_questions_by_tag(tag.tag_id)
    if questions == None:
        return HttpResponse(f"Нет такой страницы")
    elif questions.count() == 0:
        return HttpResponse(f"У этого тэга нет вопросов")
    page_obj = pagination(questions, request, QUEST_NUMBER)
    top_tags = Tag.manager.get_top()
    return render(request, 'index.html', {'data': {'title': 'Tag: {}'.format(tag_name),'top_tags': top_tags, 'quest': questions, 'page_obj': page_obj}})

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