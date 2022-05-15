from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.IndexView, name="index"),
    path('home/', views.HomeView, name="home"),
    path('find/', views.FindView, name="find"),
    path('find/accountdetails/<int:pk>/', views.AccountDetailView, name="accountdetails"),
    path('find/accountdetails/<int:pk>/sendfriendrequest/', views.SendFriendRequestView, name="send_request"),
    path('myrequests/', views.MyRequestsView, name='myrequests'),
    path('myrequests/acceptfriendrequest/<int:pk>/', views.AcceptFriendRequestView, name="accept_request"),
    path('myfriends', views.MyFriendsView, name="myfriends"),
    path('myfriends/unfriend/<int:pk>', views.UnfriendView, name="unfriend"),
    path('chat/', views.PublicChatView, name="publicchat"),
    
]
