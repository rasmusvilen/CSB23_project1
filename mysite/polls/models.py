import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
class UserAccount(models.Model):
    username = models.CharField(max_length=100, unique=True)
    # Flaw 2, Sensitive Data exposure, row 29
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

# Fix to flaw 2, rows 35-37
"""class UserAccount(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username"""