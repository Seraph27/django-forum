from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def upvote_allowed(user):                        
    return True if user.userattribute.reputation > 20 else False

def add_rep_for_question(user):
    ua = get_object_or_404(UserAttribute, user=user) 
    ua.reputation += 10
    ua.save()




def get_colors_for_rep(user):
    # print('\n'.join(dir(Colors.BLUE)))
    # print(Colors.BLUE[0],Colors.BLUE[1])
    if user.userattribute.reputation > 20:
        
        return [Colors.BLUE]
    else:
        return [Colors.DARK]
  
