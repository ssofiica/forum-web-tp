from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', views.questions, name='list_url'),
    path('hot/', views.hot, name='hot_url'),
    path('tag/', views.tag, name='tag_url'),
    path('question/<int:id>/', views.question, name='question_url'),
    path('ask/', views.ask, name='ask_url'),
    path('login/', views.login, name='login_url'),
    path('signup/', views.signup, name='signup_url'),
    path('settings/', views.settings, name='settings_url'),
]