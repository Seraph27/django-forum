from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.CharField(max_length=99999)

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
