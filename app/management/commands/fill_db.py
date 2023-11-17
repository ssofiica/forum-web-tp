from django.core.management.base import BaseCommand
from django.contrib.auth import hashers
from app import models 
import random

class Command(BaseCommand):
    help = 'Filling db'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='bd filling coefficient')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        # users = [models.User(username=f'User{i}',
        #                 first_name=f'Name{i}',
        #                 last_name=f'Surname{i}',
        #                 email=f'user{i}@gmail.com',
        #                 password=hashers.make_password(f'pass{i}'))
        #                 for i in range(ratio)]
        # models.User.objects.bulk_create(users)
        # self.stdout.write("User bd filled\n")

        # profiles = [models.Profile(user = users[i]) for i in range(ratio)]
        # profiles = models.Profile.objects.bulk_create(profiles)
        # self.stdout.write("Profile bd filled\n")

        # tags = [models.Tag(name="tag{}".format(i)) for i in range(ratio)]
        # tags = models.Tag.objects.bulk_create(tags)
        # self.stdout.write("Tags db filled\n")

        # questions = [models.Question(profile=profiles[i], 
        #                              title = "Title of question №{}".format(10*i + j),
        #                              description = "Text that describes question №{}".format(10*i + j)) 
        #                              for i in range(ratio) 
        #                                 for j in range(10)]
        # models.Question.objects.bulk_create(questions)
        # for i in range(ratio):
        #     question_index = random.sample(range(len(questions)), 10)
        #     for index in question_index:
        #         questions[index].tags.add(tags[i])
        # self.stdout.write("Question bd filled\n")

        profiles = models.Profile.objects.all()
        questions = models.Question.objects.all()

        answers = [models.Answer(profile=random.choice(profiles), 
                                 related_question = random.choice(questions), 
                                 text = "Hope this answer №{} help you".format(i) ) 
                                 for i in range(ratio * 100)]
        models.Answer.objects.bulk_create(answers)
        self.stdout.write("Answer db filled\n")

        reaction_to_q = []
        reaction_to_a = []
        for i in range(ratio):
            #r - reacted
            r_questions_index = random.sample(range(len(questions)), 100)
            r_answers_index = random.sample(range(len(answers)), 100)
            for index in r_questions_index:
                reaction_to_q.append(models.ReactionToQuestion(profile=profiles[i], question=questions[index], reaction = '+'))
                questions[index].rating += 1
            for index in r_answers_index:
                reaction_to_a.append(models.ReactionToAnswer(profile=profiles[i], answer=answers[index], reaction = '+'))
                answers[index].rating += 1
        
        models.ReactionToQuestion.objects.bulk_create(reaction_to_q)
        models.ReactionToAnswer.objects.bulk_create(reaction_to_a)
        self.stdout.write("Likes filled\n")

        self.stdout.write("DONE")
        