from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
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

def question_detail(request, pk):

	question = get_object_or_404(Question, pk=pk)

	# answers = question.answer_set.all()

	return render(request, 'rex_app/question_detail.html', {
		'question': question,
		'questions': Question.objects.all(),

		}) 

# forms.BaseForm -> (forms.Form, forms.ModelForm)

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['text']

	# text = forms.CharField(widget=forms.Textarea)



def create_question(request):

	print('here:')
	print(request.method)

	if request.method == 'POST':

		print(request.POST)

		form = QuestionForm(request.POST)
		# form is now BOUND

		if form.is_valid():
			# form is now valid
			print(form.cleaned_data['text'])

			form.save()

			# Question.objects.create(text=form.cleaned_data['text'])

			# q = Question(text=form.cleaned_data['text'])
			# q.save()

			print('good form')
		else:
			print('bad form')


	else:
		form = QuestionForm()

	return render(request, 'rex_app/create_question.html', {
		'form': form,
	}) 



class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text', 'upvotes', 'accepted']


def create_answer(request, question_pk):
	if request.method == 'POST':

		form = AnswerForm(request.POST)
		# form is now BOUND

		if form.is_valid():
			# form is now valid

			answer = form.save(commit=False)
			answer.question = Question.objects.get(pk=question_pk)
			answer.save()


			print('good form')
		else:
			print('bad form')


	else:
		form = AnswerForm()

	return render(request, 'rex_app/create_answer.html', {
		'form': form,
		'question_pk': question_pk,
	}) 
