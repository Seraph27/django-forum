from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# TODO User field for Answer and Comment, update views, render users that answered questions etc

class Colors(models.IntegerChoices):
    GREEN = 1, 'green'
    BLUE = 2, 'blue'
    
class DirectMessage(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='from_user_reverse')
	to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to_user_reverse')
	text = models.CharField(max_length=99999)

	def __str__(self):
		return str(self.from_user)+'>'+str(self.to_user)+' '+self.text

class UserAttribute(models.Model):
	user = models.OneToOneField(User, on_delete=models.PROTECT)
	background_color = models.IntegerField(choices=Colors.choices)

class Question(models.Model):
    text = models.CharField(max_length=99999)
    asked_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:200]

class Answer(models.Model):
    text = models.CharField(max_length=99999)
    upvotes = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:200] + str(self.upvotes) + str(self.accepted)

class Comment(models.Model):
    text = models.CharField(max_length=99999)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:200]
