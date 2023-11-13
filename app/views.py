from django.shortcuts import render

def questions(request):
    return render(request, 'index.html', {'data': range(5)})

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def question(request):
    return render(request, 'question.html', {'data': range(5)})