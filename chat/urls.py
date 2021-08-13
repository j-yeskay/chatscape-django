from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
	path('', views.IndexView, name = "index"),
	path('home/', views.HomeView, name = "home"),
	path('home/editdetails/', login_required(views.EditDetailsView.as_view(),login_url = "home"), name = "editdetails"),
	path('home/password/', login_required(views.ChangePasswordView.as_view(),login_url = "home"), name = "changepassword"),
	path('find/', views.FindView, name = "find"),
	path('find/accountdetails/<int:pk>/', views.AccountDetailView, name = "accountdetails"),
	path('find/accountdetails/<int:pk>/sendfriendrequest/', views.SendFriendRequestView, name = "send_request"),
	path('myrequests/',views.MyRequestsView, name = 'myrequests'),
	path('myrequests/acceptfriendrequest/<int:pk>/',views.AcceptFriendRequestView, name = "accept_request"),
	path('myfriends', views.MyFriendsView, name = "myfriends"),
	path('myfriends/unfriend/<int:pk>', views.UnfriendView, name = "unfriend"),
	path('chat/', views.PublicChatView, name = "publicchat"),
	path('login/', views.LoginPage, name = "login"),
	path('logout/', views.LogoutView, name = "logout"),
	path('register/', views.RegisterPage, name = "register"),

]
