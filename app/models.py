from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import ObjectDoesNotExist

class ProfileManager(models.Manager):
    def get_top5(self):
        return self.order_by('-rep')[:5]
    def get_user_by_username(self, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = None

        return user
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    avatar = models.ImageField(upload_to='uploads', blank=True, null=True, default='static/image/default_ava.png')
    rating = models.IntegerField(default=0)

    manager = ProfileManager()

class TagManager(models.Manager):
    def get_top(self):
        return self.annotate(count=Count('questions')).order_by('-count')[:10]

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    manager = TagManager()

    def __str__(self):
        return f'({self.tag_id}) {self.name}'

class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_date')

    def get_hot(self):
        return self.annotate(count=Count('answers')).order_by('-rating')[:20]

    def get_questions_by_tag(self, tag):
        return self.filter(tags=tag).order_by('-rating')
    

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='questions')
    title = models.CharField(max_length=128)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    manager = QuestionManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='answers')
    related_question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='answers')
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

class ReactionToAnswer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reaction_to_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer')

    LIKE = '+'
    DISLIKE = '-'
    REACTION = [
        (LIKE, "like"),
        (DISLIKE, "dislike"),
    ]
    reaction = models.CharField(max_length=1, choices=REACTION)

    def __str__(self):
        return f'({self.profile.user.username} {self.reaction} answer by {self.answer.profile}'

class ReactionToQuestion(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reaction_to_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')

    LIKE = '+'
    DISLIKE = '-'
    REACTION = [
        (LIKE, "like"),
        (DISLIKE, "dislike"),
    ]
    reaction = models.CharField(max_length=1, choices=REACTION)

    def __str__(self):
        return f'({self.profile.user.username} {self.reaction} question {self.question.title}'