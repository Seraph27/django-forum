from django.db import models
from django.contrib.auth.models import User

class GlobalPermissions(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('moderator', 'Can moderate'),
            ('voter', 'Can upvote/downvote'),
        )

class Colors(models.IntegerChoices):
    DARK = 1, '#212529'
    BLUE = 2, '#001442'
    GREEN = 3, '#00321b'

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


class DirectMessage(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='from_user_reverse')
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to_user_reverse')
    time_stamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=99999)

    def __str__(self):
    	return str(self.from_user)+'>'+str(self.to_user)+' '+self.text


class UserAttribute(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    background_color = models.IntegerField(choices=Colors.choices, default=Colors.DARK)    
    avatar = models.CharField(max_length=99999, choices=Avatars.choices, default=Avatars.PX)
    birthday=models.DateField(null=True, blank=True)
    reputation = models.IntegerField(default=0)
    friends = models.ManyToManyField(
        User,
        through='FriendAdditionalDetail', 
        through_fields=('user_attribute', 'user'),
        related_name='friends_reverse',
        )
    def is_upvote_allowed(self):                        
        return True if self.reputation > 20 else False

    def add_rep_for_question(self):
        self.reputation += 10
        self.save()
    


    def is_shop_unlocked(self):
        return True if self.reputation > 50 else False  
              
    def get_avatar_list(self):
        return [(Avatars.PX, 'PX avatar','fab fa-500px', True ),
                (Avatars.ANGRY, 'Angry avatar', 'far fa-angry', self.reputation > 25),
                (Avatars.atom, 'Atom avatar',  'fas fa-atom', self.reputation > 50)]

    def get_color_list(self):
        return [(Colors.BLUE, 'Blue', '#001442', True), 
                (Colors.DARK, 'Dark', '#212529', self.reputation > 25),
                (Colors.GREEN, 'Green', '#00321b', self.reputation > 50),]
    

class FriendStatus(models.IntegerChoices):
    AWAITING_APPROVAL = 1, 'AWAITING_APPROVAL'
    REJECTED = 2, 'REJECTED'
    APPROVED = 3, 'APPROVED'

class FriendAdditionalDetail(models.Model):
    class Meta:
        unique_together = ('user_attribute', 'user')
    user_attribute = models.ForeignKey(UserAttribute, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.IntegerField(choices=FriendStatus.choices)    

    def save(self, *args, **kwargs):
        if self.user_attribute.user == self.user:
            raise ValidationError('Can\'t become friends with yourself.')
        super().save(*args, **kwargs)

class Tag(models.Model):
    text = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.text[:200]

class Question(models.Model):
    title = models.CharField(max_length=99)
    text = models.CharField(max_length=99999)
    asked_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)

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
