from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# TODO User field for Answer and Comment, update views, render users that answered questions etc

class UserAttribute(models.Model):
	user = models.OneToOneField(User, on_delete=models.PROTECT)
	background_color = models.CharField(max_length=999)


class Question(models.Model):
    text = models.CharField(max_length=99999)
    asked_by = models.ForeignKey(User, on_delete=models.PROTECT)


    def __str__(self):
        return self.text[:200]


class Answer(models.Model):
    text = models.CharField(max_length=99999)
    upvotes = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:200] + str(self.upvotes) + str(self.accepted)

class Comment(models.Model):
    text = models.CharField(max_length=99999)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:200]
