from django.urls import path

from . import views

urlpatterns = [

    path('index', views.index, name='index'),
    path('inc_age', views.inc_age, name='inc_age'),
    path('question/create', views.create_question, name='create_question'),
    path('answer/create/<int:question_pk>', views.create_answer, name='create_answer'),
    path('comment/create/<int:answer_pk>', views.create_comment, name='create_comment'),
    path('question/<int:pk>', views.question_detail, name='question_detail'),
    path('search', views.search, name='search'),
    path('upvote/<int:answer_pk>', views.upvote, name='upvote'),
    path('downvote/<int:answer_pk>', views.downvote, name='downvote'),
    path('accept/<int:answer_pk>', views.mark_accepted, name='accept'),
    path('settings/<username>', views.settings, name='settings'),
    path('change_color/<username>', views.change_color, name='change_color'),


    
    
]

