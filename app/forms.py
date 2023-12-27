from django import forms
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import hashers
from . import models


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class ProfileForm(forms.Form):
    username = forms.CharField(min_length=4)
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')

        if models.Profile.manager.get_user_by_username(username):
            self.add_error('username', IntegrityError("User already exists"))

        return self.cleaned_data

    def save(self, id):
        user = models.User.objects.get(user_id=id)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')

        profile = models.Profile(user_id=id)
        avatar = self.files.get('avatar')
        if avatar:
            profile.avatar=avatar
            
        user.save()
        profile.save()


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=4)
    password = forms.CharField(min_length=8)
    password_check = forms.CharField(min_length=8)
    email = forms.EmailField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    avatar = forms.ImageField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_check')

        if models.Profile.manager.get_user_by_username(username):
            self.add_error('username', IntegrityError("User already exists"))

        if password_1 != password_2:
            self.add_error(None, ValidationError("Passwords is invalid", code='invalid'))

        return self.cleaned_data

    def save(self):
        super().clean()
        new_user = models.User(username=self.cleaned_data['username'],
                    email=self.cleaned_data['email'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    password=hashers.make_password(self.cleaned_data['password']))
        new_user.save()

        new_user_id = new_user.id

        new_profile = models.Profile(user_id=new_user_id)
        avatar = self.files.get('avatar')
        if avatar:
            new_profile.avatar=avatar

        new_profile.save()


class QuestionForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    tags = forms.CharField(required=False)

    def save(self, profile_id) -> int:
        super().clean()
        print(self.cleaned_data['tags'])

        tags_names = self.cleaned_data['tags'].split()
        tags = []
        for tag_name in tags_names:
            if models.Tag.manager.filter(name=tag_name).exists():
                tags.append(models.Tag.manager.get(name=tag_name))
            else:
                new_tag = models.Tag(name=tag_name)
                new_tag.save()
                tags.append(new_tag)

        new_question = models.Question(profile_id=profile_id,
                                        title=self.cleaned_data['title'],
                                        text=self.cleaned_data['description'])
        new_question.save()
        new_question.tags.set(tags)

        return new_question.question_id

class AnswerForm(forms.Form):
    text = forms.CharField()

    def save(self, profile_id, q_id) -> id:
        super().clean()
        new_answer = models.Answer(profile_id=profile_id,
                                    related_question_id=q_id,
                                    text=self.cleaned_data['text'])
        new_answer.save()

        return new_answer.answer_id