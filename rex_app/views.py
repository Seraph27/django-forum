from django.shortcuts import render
from django.http import HttpResponse

from random import randint

from .models import *

# Create your views here.
def index(request):
	# return HttpResponse('<b>Welcome!</b>')
	return render(request, 'rex_app/b.html', {
		'people': Person.objects.all(),
		'sunny_today': True,
		'a_big_number': 23094820394803948309,
		'fruits': ['apple','banana','orange'],
		'd': {'a': 1, 'b': 2},
		})

def inc_age(request):

	rex = Person.objects.get(first='r')

	rex.age += 1

	rex.save()

	return render(request, 'rex_app/b.html', {
		'people': Person.objects.all(),
		})	 