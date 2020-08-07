from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, reverse
from django.contrib import messages
from random import randint
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from .models import *
from .reputation import upvote_allowed, add_rep_for_question

from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import IntegrityError
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder


class DirectMessageList(LoginRequiredMixin, ListView):
    model = DirectMessage

    def get_queryset(self):
        qs = super().get_queryset() 
        
        return qs.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))


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
        # 'python_tag':Tag.objects.get(text='python'),
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
        fields = ['title', 'text', 'tag']
        widgets = {
            'text': forms.Textarea(attrs={'cols':200, 'rows': 20}),

        }


@login_required
def create_question(request):

    if request.method == 'POST':

        form = QuestionForm(request.POST)

        if form.is_valid():
            add_rep_for_question(request.user)
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

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['text']

@login_required
def create_tag(request):

    if request.method == 'POST':

        form = TagForm(request.POST)

        if form.is_valid():
            tag = form.save(commit=False)
            for t in Tag.objects.all():
                if t.text == form.cleaned_data['text']:
                    messages.add_message(request, messages.ERROR, 'Tag already exists!')
                    return redirect('create_question')

            tag.text = form.cleaned_data['text']
            tag.save()
            messages.add_message(request, messages.SUCCESS, 'Tag successfully created!')
            return redirect('create_question')
            

        else:
            messages.add_message(request, messages.ERROR, 'Terrible form D; ')

    else:
        form = TagForm()

    return render(request, 'rex_app/create_tag.html', {    
        'form': form,
    }) 

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

class Profile(LoginRequiredMixin, DetailView): #profile
    model = UserAttribute  
    template_name = 'rex_app/profile.html' 

@login_required
def friends_list(request):
    friends = FriendAdditionalDetail.objects.filter(status=FriendStatus.APPROVED, user_attribute__user=request.user)
    friends_incoming_waiting_approval = FriendAdditionalDetail.objects.filter(status=FriendStatus.AWAITING_APPROVAL,user=request.user)
    friends_rejected = FriendAdditionalDetail.objects.filter(status=FriendStatus.REJECTED, user_attribute__user=request.user)
    friends_outgoing_waiting_approval = FriendAdditionalDetail.objects.filter(status=FriendStatus.AWAITING_APPROVAL,user_attribute__user=request.user)
    return render(request, 'rex_app/friends_list.html', {    
        'friends': friends,
        'friends_incoming_waiting_approval': friends_incoming_waiting_approval,
        'friends_rejected': friends_rejected,
        'friends_outgoing_waiting_approval': friends_outgoing_waiting_approval,
    }) 

@login_required
def add_friend(request, pk):

    my_attributes = UserAttribute.objects.get(user__username=request.user)   #user (in UserAttribute) >> username (in User) use ris in userattribute
    friend_to_add = User.objects.get(pk=pk)
#check pair in friendadditional or don't create
    try: 
        FriendAdditionalDetail.objects.create(
            user_attribute=my_attributes, user=friend_to_add, status=FriendStatus.AWAITING_APPROVAL)
    except IntegrityError:
        messages.add_message(request, messages.ERROR, 'Cannot add friend: you already added ' + friend_to_add.username + ' as friend!')
    return redirect('friends_list')

@login_required
def remove_friend(request, pk):

    my_attributes = UserAttribute.objects.get(user__username=request.user)   #user (in UserAttribute) >> username (in User) use ris in userattribute
    friend_to_remove = User.objects.get(pk=pk)

    FriendAdditionalDetail.objects.filter(user_attribute=my_attributes, user=friend_to_remove).delete()

    messages.add_message(request, messages.ERROR, 'Removed ' + friend_to_remove.username + ' as friend!')

    return redirect('friends_list')

@login_required
def reject_friend(request, pk):

    friend_request = get_object_or_404(FriendAdditionalDetail, pk=pk)
    friend_request.delete()

    messages.add_message(request, messages.ERROR, 'Rejected ' + friend_request.user_attribute.user.username + '\'s friend request!')

    return redirect('friends_list')

@login_required
def accept_friend(request, pk):
    friend_request = get_object_or_404(FriendAdditionalDetail, pk=pk)
    friend_request.status = FriendStatus.APPROVED
    friend_request.save()

    return redirect('friends_list')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

@login_required
def create_answer(request, question_pk):
    if request.method == 'POST':

        form = AnswerForm(request.POST)

        if form.is_valid():
            add_rep_for_question(request.user)
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
            
            add_rep_for_question(request.user)
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

        search_results_for_question = Question.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
        search_results_for_answer = Answer.objects.filter(text__icontains=query)
        search_results_for_tag = Tag.objects.filter(text__icontains=query)

        return render(request, 'rex_app/search.html', {
                'search_results_for_question': search_results_for_question,
                'search_results_for_answer':search_results_for_answer,
                'search_results_for_tag':search_results_for_tag, 
                'query': query,
            })

@login_required
def search_for_user(request):
    if request.method == 'GET':
        
        query = request.GET.get('searchbox')
        search_results_for_username = User.objects.filter(username__icontains=query)

        return render(request, 'rex_app/search_for_user.html', {
                'search_results_for_username': search_results_for_username,
                'query': query,
            })


@login_required
def upvote(request, answer_pk):

    upvote = get_object_or_404(Answer, pk=answer_pk)

    if request.method == 'POST':
        if upvote_allowed(request.user):
            upvote.upvotes += 1
            upvote.save()
        else:
            messages.add_message(request, messages.ERROR, 'Requires 20 reputation!')
    return redirect('question_detail', pk=upvote.question.pk)


@login_required
def downvote(request, answer_pk):
    downvote = get_object_or_404(Answer, pk=answer_pk)

    if request.method == 'POST':
        if upvote_allowed(request.user):
            downvote.upvotes -= 1
            downvote.save()
        else:
            messages.add_message(request, messages.ERROR, 'Requires 20 reputation!')
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



