from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, reverse
from django.contrib import messages
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from .models import *

from django.views.generic import ListView, CreateView, UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder


class DirectMessageList(LoginRequiredMixin, ListView):
    model = DirectMessage

    def get_queryset(self):
        qs = super().get_queryset() 
        
        return qs.filter(from_user=self.request.user)


class DirectMessageForm(forms.ModelForm): 
    class Meta:

        model = DirectMessage
        fields = ['to_user', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('direct_message_create')
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-warning')) 
        # self.helper.layout = Layout(
        #     Fieldset(
        #         'TITLE REX',
        #         'to_user',
        #         'text',
        #     ),
        #     ButtonHolder(
        #         Submit('submit', 'Submit', css_class='button white')
        #     )
        # )


class DirectMessageCreate(LoginRequiredMixin, CreateView):
    model = DirectMessage
    form_class = DirectMessageForm
    # if dont specify form_class then fields is required
    # fields = ['from_user', 'to_user', 'text']

    def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
        form.instance.from_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('direct_message_list')

# Create your views here.
@login_required
def home_detail(request):
    top_three_recent = Question.objects.all().order_by('-id')[:3]
    current_user = UserAttribute.objects.get(user=request.user)

    return render(request,'rex_app/home.html', {
        'python_tag':Tag.objects.get(text='python'),
        'recents': top_three_recent,
        'questions': Question.objects.all(),     
        }) 
@login_required
def question_detail(request, pk):

    question = get_object_or_404(Question, pk=pk)

    return render(request, 'rex_app/question_detail.html', {
        'question': question,
        'questions': Question.objects.all(),
        'answers': Answer.objects.all(),

        }) 

# forms.BaseForm -> (forms.Form, forms.ModelForm)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'tag']


@login_required
def create_question(request):

    if request.method == 'POST':

        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.asked_by = request.user
            question.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'Question successfully created!')
            return redirect('question_detail', pk=question.pk)

        else:
            messages.add_message(request, messages.ERROR, 'Terrible form D; ')

    else:
        form = QuestionForm()

    return render(request, 'rex_app/create_question.html', {    
        'form': form,
    }) 

class EditQuestion(UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm

    def test_func(self):
        return self.request.user == self.get_object().asked_by 

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'question successfully edited!')
        return reverse('question_detail', kwargs={'pk':self.get_object().pk}) 

class UserAttributeForm(forms.ModelForm):
    class Meta:
        model = UserAttribute
        fields = ['background_color', 'avatar', 'birthday' ]


class EditUserAttributes(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = UserAttribute
    form_class = UserAttributeForm
    success_message = "Settings updated"

    def test_func(self):
        return self.request.user == self.get_object().user 

    def get_success_url(self):
        return reverse('settings', kwargs={'pk':self.get_object().pk}) 

class UserAttributeList(LoginRequiredMixin, ListView): #profile
    model = UserAttribute   

def friends_list(request):
    friends = Friends.objects.get(current_user=request.user)
    users = User.objects.all()
    return render(request, 'rex_app/friends_list.html', {    
        'friends': friends,
        'users': users,
    }) 

def add_friend(request, pk):
    friend = User.objects.get(pk=pk)
    Friend.add_friend(request.user, friend)

def remove_friend(request, pk):
    friend = User.objects.get(pk=pk)
    Friend.remove_friend(request.user, friend)
    
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

@login_required
def create_answer(request, question_pk):
    if request.method == 'POST':

        form = AnswerForm(request.POST)

        if form.is_valid():

            answer = form.save(commit=False)
            answer.question = Question.objects.get(pk=question_pk)
            answer.answered_by = request.user
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

@login_required
def edit_answer(request, answer_pk):

    answer = get_object_or_404(Answer, pk=answer_pk)

    if request.method == 'POST':

        form = AnswerForm(request.POST)

        if form.is_valid() and request.user == answer.answered_by:

            answer.text = form.cleaned_data['text']
            answer.save()
            messages.add_message(request, messages.SUCCESS, 'Answer successfully edited!')
            return redirect('question_detail', pk=answer.question.pk)

        else:
            messages.add_message(request, messages.ERROR, 'dont you dare change someone elses answer')

    else:
        form = AnswerForm(instance=answer)        
    return render(request, 'rex_app/edit_answer.html', {
        'form': form,
        'answer_pk': answer_pk,       

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
            comment.commented_by = request.user
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
        search_results_for_tag = Tag.objects.filter(text=query)

        return render(request, 'rex_app/search.html', {
                'search_results_for_question': search_results_for_question,
                'search_results_for_answer':search_results_for_answer,
                'search_results_for_tag':search_results_for_tag, 
                'query': query,
            })

@login_required
def upvote(request, answer_pk):

    upvote = get_object_or_404(Answer, pk=answer_pk)

    if request.method == 'POST':
        upvote.upvotes += 1
        upvote.save()
    
    return redirect('question_detail', pk=upvote.question.pk)


@login_required
def downvote(request, answer_pk):
    downvote = get_object_or_404(Answer, pk=answer_pk)

    if request.method == 'POST':
        downvote.upvotes -= 1
        downvote.save()
    
    return redirect('question_detail', pk=downvote.question.pk)


@login_required
def mark_accepted(request, answer_pk):
    accept = get_object_or_404(Answer, pk=answer_pk)

    if request.method == 'POST':
        accept.accepted = True
        accept.save()

    return redirect('question_detail', pk=accept.question.pk)

# @login_required
# def settings(request):

#     return render(request, 'rex_app/settings.html', {
    
#     }) 

# class ChangeColorForm(forms.ModelForm):
#     class Meta:
#         model = UserAttribute
#         fields = ['background_color']


# @login_required
# def change_color(request, user_pk):

#     user = get_object_or_404(User, pk=user_pk)  
#     ua = UserAttribute.objects.get(user=user)
    
#     if request.method == 'POST':

#         form = ChangeColorForm(request.POST)

#         if form.is_valid():

            
#             ua.background_color = form.cleaned_data['background_color']
#             ua.save()

#             messages.add_message(request, messages.SUCCESS, 'Background color successfully updated!')
#             return redirect('settings', user_pk=user_pk)

#         else:
#             messages.add_message(request, messages.ERROR, 'Terrible form D; ')

#     else:
#         form = ChangeColorForm(instance=ua)

#     return render(request, 'rex_app/change_color.html', {   
#         'form': form,
#     })  



