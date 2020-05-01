from django.shortcuts import render
from django.http import HttpResponse

from random import randint

# Create your views here.
def index(request):
	# return HttpResponse('<b>Welcome!</b>')
	return render(request, 'rex_app/b.html', {
		'sunny_today': True,
		'a_big_number': 23094820394803948309,
		'fruits': ['apple','banana','orange'],
		'd': {'a': 1, 'b': 2},
		})