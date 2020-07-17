from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# TODO User field for Answer and Comment, update views, render users that answered questions etc

class Colors(models.IntegerChoices):
    GREEN = 1, 'green'
    BLUE = 2, 'blue'

class Avatars(models.TextChoices):
    PX = 1, 'fab fa-500px'
    ANGRY = 2, 'far fa-angry'
    backspace = 3, 'fas fa-backspace'
    atom = 4, 'fas fa-atom'
    battle_net = 5, 'fab fa-battle-net'
    biohazard = 6, 'fas fa-biohazard'
    braille = 7, 'fas fa-braille'
    burn = 8, 'fas fa-burn'
    mapleleaf = 9, 'fab fa-canadian-maple-leaf'
    carcrash = 10, 'fas fa-car-crash'

class Timezone(models.TextChoices):
    TAIWAN = 1, 'Asia/Taipei'
    GMT = 2, 'Etc/GMT'
    GMTplus0 = 3, 'Etc/GMT+0'
    GMTplus1 = 4, 'Etc/GMT+1'
    GMTplus10 = 5, 'Etc/GMT+10'
    GMTplus11 = 6, 'Etc/GMT+11'
    GMTplus12 = 7, 'Etc/GMT+12'
    GMTplus2 = 8, 'Etc/GMT+2'
    GMTplus3 = 9, 'Etc/GMT+3'
    GMTplus4 = 10, 'Etc/GMT+4'
    GMTplus5 = 11, 'Etc/GMT+5'
    GMTplus6 = 12, 'Etc/GMT+6'
    GMTplus7 = 13, 'Etc/GMT+7'
    GMTplus8 = 14, 'Etc/GMT+8'
    GMTplus9 = 15, 'Etc/GMT+9'
    GMTminus0 = 16, 'Etc/GMT-0'
    GMTminus1 = 17, 'Etc/GMT-1'
    GMTminus10 = 18, 'Etc/GMT-10'
    GMTminus11 = 19, 'Etc/GMT-11'
    GMTminus12 = 20, 'Etc/GMT-12'
    GMTminus13 = 21, 'Etc/GMT-13'
    GMTminus14 = 22, 'Etc/GMT-14'
    GMTminus2 = 23, 'Etc/GMT-2'
    GMTminus3 = 24, 'Etc/GMT-3'
    GMTminus4 = 25, 'Etc/GMT-4'
    GMTminus5 = 26, 'Etc/GMT-5'
    GMTminus6 = 27, 'Etc/GMT-6'
    GMTminus7 = 28, 'Etc/GMT-7'
    GMTminus8 = 29, 'Etc/GMT-8'
    GMTminus9 = 30, 'Etc/GMT-9'

class DirectMessage(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='from_user_reverse')
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to_user_reverse')
    text = models.CharField(max_length=99999)

    def __str__(self):
    	return str(self.from_user)+'>'+str(self.to_user)+' '+self.text

class UserAttribute(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    background_color = models.IntegerField(choices=Colors.choices)    
    avatar = models.CharField(max_length=99999, choices=Avatars.choices)
    birthday=models.DateField(auto_now=False, null=True, blank=True)
    timezone=models.CharField(max_length=99999, choices=Timezone.choices)

class Question(models.Model):
    text = models.CharField(max_length=99999)
    asked_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=20, null=True)

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
