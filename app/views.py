from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from app.models import Question, Tag, Answer, Profile
from django.contrib import auth
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from app import forms

QUEST_NUMBER = 20
ANSWER_NUMBER = 30

def pagination(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def context_for_sidebar(context):
    context['popular_tags'] = Tag.manager.get_top()
    context['popular_users'] = Profile.manager.get_top5()

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

def question(request, question_id : int, page_num = 1):
    # question = get_object_or_404(models.Question, id=question_id)
    question = Question.manager.get_by_id_or_None(question_id)
    if question == None:
        return HttpResponseNotFound("Нет такого вопроса")

    if request.method == 'POST':
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            id = answer_form.save(request.user.profile.id, question_id)
            answers = pagination(Answer.manager.get_by_question(question), page_num)

            return redirect(reverse('question_url',
                                    kwargs={'question_id':question_id,
                                            'page_num':answers.paginator.num_pages}) + f'#{id}')

    answers_for_page = pagination(Answer.manager.get_by_question(question), page_num)
    if answers_for_page == None:
        return HttpResponseNotFound(f"Нет такой страницы")

    context = { 'title': question.title,
                'question': question,
                'answers': answers_for_page,
                'page_num': page_num,
                'page_url': "question_page",
    }
    context_for_sidebar(context)

    return render(request, 'question.html' , context=context)

@login_required
def ask(request):
    if request.method == 'GET':
        question_form = forms.QuestionForm()

    if request.method == 'POST':
        question_form = forms.QuestionForm(request.POST)
        if question_form.is_valid():
            q_id = question_form.save(request.user.profile.id)
            return redirect('question', q_id)

    context = { 'form': question_form }
    context_for_sidebar(context)

    return render(request, "ask.html", context=context)

def signup(request):
    if request.method == 'GET':
        user_form = forms.RegistrationForm()
    
    if request.method == 'POST':
        user_form = forms.RegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()

            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Error while creating user")
    
    context = { 'form': user_form }
    context_for_sidebar(context)

    return render(request, "signup.html", context=context)

def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def login(request):
    if request.method == 'GET':
        user_form = forms.LoginForm()

    if request.method == 'POST':
        user_form = forms.LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Wrong username or password")
    
    context = { 'form': user_form }
    context_for_sidebar(context)
    return render(request, "login.html", context=context)

def edit_profile(request):
    if request.method == 'GET':
        edit_form = forms.ProfileForm()

    if request.method == 'POST':
        edit_form = forms.ProfileFormForm(request.POST)
        if edit_form.is_valid():
            edit_form.save(request.user.profile.id)
            return redirect('edit_profile_url')

    context = { 'form': edit_form }
    context_for_sidebar(context)

    return render(request, "settings.html", context=context)