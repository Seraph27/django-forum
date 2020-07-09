from django.urls import path

from . import views

urlpatterns = [

    path('home', views.home_detail, name='home'),
    path('question/create', views.create_question, name='create_question'),
    path('answer/create/<int:question_pk>', views.create_answer, name='create_answer'),
    path('answer/edit/<int:answer_pk>', views.edit_answer, name='edit_answer'),
    path('comment/create/<int:answer_pk>', views.create_comment, name='create_comment'),
    path('question/<int:pk>', views.question_detail, name='question_detail'),
    path('question/edit/<int:pk>', views.EditQuestion.as_view(), name='edit_question'),
    path('search', views.search, name='search'),
    path('upvote/<int:answer_pk>', views.upvote, name='upvote'),
    path('downvote/<int:answer_pk>', views.downvote, name='downvote'),
    path('accept/<int:answer_pk>', views.mark_accepted, name='accept'),
    path('settings/<int:user_pk>', views.settings, name='settings'),
    path('change_color/<int:user_pk>', views.change_color, name='change_color'),

    path('dm/list', views.DirectMessageList.as_view(), name='direct_message_list'),
    path('dm/create', views.DirectMessageCreate.as_view(), name='direct_message_create'),

    


    
    
]

