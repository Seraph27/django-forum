from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib import messages
from random import randint
from django.contrib.auth.decorators import login_required

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
		'answers': Answer.objects.all(),

		}) 

# forms.BaseForm -> (forms.Form, forms.ModelForm)

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['text']


@login_required
def create_question(request):

	if request.method == 'POST':

		form = QuestionForm(request.POST)

		if form.is_valid():
			question = form.save(commit=False)
			question.asked_by = request.user
			question.save()
			messages.add_message(request, messages.SUCCESS, 'Question successfully created!')
			return redirect('question_detail', pk=question.pk)

		else:
			messages.add_message(request, messages.ERROR, 'Terrible form D; ')

	else:
		form = QuestionForm()

	return render(request, 'rex_app/create_question.html', {	
		'form': form,
	}) 



class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text', 'upvotes', 'accepted']

@login_required
def create_answer(request, question_pk):
	if request.method == 'POST':

		form = AnswerForm(request.POST)

		if form.is_valid():

			answer = form.save(commit=False)
			answer.question = Question.objects.get(pk=question_pk)
			answer.save()
			messages.add_message(request, messages.SUCCESS, 'Answer successfully created!')
			return redirect('question_detail', pk=question_pk)


		else:
			messages.add_message(request, messages.ERROR, 'Terrible form D; ')


	else:
		form = AnswerForm()

	return render(request, 'rex_app/create_answer.html', {
		'form': form,
		'question_pk': question_pk,
	}) 


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text']


@login_required
def create_comment(request, answer_pk):
	if request.method == 'POST':

		form = CommentForm(request.POST)

		if form.is_valid():

			comment = form.save(commit=False)
			comment.answer = Answer.objects.get(pk=answer_pk)
			comment.save()
			messages.add_message(request, messages.SUCCESS, 'Comment successfully created!')			

			return redirect('question_detail', pk=comment.answer.question.pk)

		else:
			messages.add_message(request, messages.ERROR, 'Terrible form D; ')

	else:
		form = CommentForm()

	return render(request, 'rex_app/create_comment.html', {
		'form': form,
		'answer_pk': answer_pk,
	}) 

@login_required
def search(request):
	if request.method == 'GET':

		query = request.GET.get('searchbox')

		search_results_for_question = Question.objects.filter(text__icontains=query)
		search_results_for_answer = Answer.objects.filter(text__icontains=query)

		return render(request, 'rex_app/search.html', {
				'search_results_for_question': search_results_for_question,
				'search_results_for_answer':search_results_for_answer,
                'query': query,
			})

@login_required
def upvote(request, answer_pk):

	upvote = get_object_or_404(Answer, pk=answer_pk)

	if request.method == 'POST':
		upvote.upvotes += 1
		upvote.save()
	
	return redirect('question_detail', pk=upvote.question.pk)


#add 404 and post request TODO
@login_required
def downvote(request, answer_pk):
	downvote = Answer.objects.get(pk=answer_pk)
	downvote.upvotes -= 1
	downvote.save()

	return redirect('question_detail', pk=downvote.question.pk)
@login_required
def mark_accepted(request, answer_pk):
	accept = Answer.objects.get(pk=answer_pk)
	accept.accepted = True
	accept.save()

	return redirect('question_detail', pk=accept.question.pk)



