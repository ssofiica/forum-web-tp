from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('questions/', views.questions, name='list_url'),
    path('question/', views.question, name='question_url'),
    path('ask/', views.ask, name='ask_url'),
    path('login/', views.login, name='login_url'),
    path('signup/', views.signup, name='signup_url'),
]