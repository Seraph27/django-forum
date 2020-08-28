from django.urls import path

from . import views

urlpatterns = [
    path('create_user', views.create_user, name='create_user'),
    path('home', views.home_detail, name='home'),
    path('question/create', views.create_question, name='create_question'),
    path('tag/create', views.create_tag, name='create_tag'),
    path('answer/create/<int:question_pk>', views.create_answer, name='create_answer'),
    path('answer/edit/<int:answer_pk>', views.edit_answer, name='edit_answer'),
    path('comment/create/<int:answer_pk>', views.create_comment, name='create_comment'),
    path('question/<int:pk>', views.question_detail, name='question_detail'),
    path('question/edit/<int:pk>', views.EditQuestion.as_view(), name='edit_question'),
    path('search', views.search, name='search'),
    path('search_for_user', views.search_for_user, name='search_for_user'),
    path('upvote/<int:answer_pk>', views.upvote, name='upvote'),
    path('downvote/<int:answer_pk>', views.downvote, name='downvote'),
    path('accept/<int:answer_pk>', views.mark_accepted, name='accept'),
    path('settings/<int:pk>', views.EditUserAttributes.as_view(), name='settings'),
    path('friends/list', views.friends_list, name='friends_list'),
    path('friends/add/<int:pk>', views.add_friend, name='add_friend'),
    path('friends/remove/<int:pk>', views.remove_friend, name='remove_friend'),
    path('friends/accept/<int:pk>', views.accept_friend, name='accept_friend'),
    path('friends/reject/<int:pk>', views.reject_friend, name='reject_friend'),
    path('dm/list', views.DirectMessageList.as_view(), name='direct_message_list'),
    path('dm/create', views.DirectMessageCreate.as_view(), name='direct_message_create'),
    path('dm/conversation/<int:other_user_pk>', views.show_conversation, name='show_conversation'),
    path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
    path('achievements/<int:pk>', views.Achievements.as_view(), name='achievements'),
    


    
    
]

