from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from . import views
urlpatterns = [

    path('home/', views.HomeView.as_view()),
    path('', RedirectView.as_view(url="home/")),
    path('accounts/register/complete', RedirectView.as_view(url="home/")),

    path('home/search/', views.HomeView.search),


    path('profile/<int:myid>', views.ProfileView.profile),
    path('profile/post/', views.ProfileView.post),
    path('profile/profile_pic_update/', views.ProfileView.prof_pic_update),
    path('profile/post_delete/<int:myid>', views.ProfileView.post_delete),

    path('profile/follow_operation/', views.follow_operation),

    path('setting/', RedirectView.as_view(url="profile/")),
    path('setting/profile/', views.SettingView.profile_update),
    path('setting/security/', views.SettingView.security),
    path('setting/about/', views.SettingView.about),
    path('changePassword/', views.changePassword),

    path('notification/', views.NotificationView.as_view()),
    path('notification/fetch/', views.NotificationView.fetch),
    path('clear_notification/', views.clear_notification),

    path('chat/', views.ChatView.as_view()),
    path('chat/search/', views.ChatView.csearch),
    path('chat/message/<int:rid>', views.ChatView.message),
    path('sendMessage/', views.ChatView.sendMessage),
    path('messageFetch/', views.ChatView.messageFetch),

    path('follow_request/', views.follow_request),

    path('like_post/', views.like_post),

    path('comment_post/', views.comment_post),


    path('sendMail/', views.sendMail),

]
