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
	path('chat/', views.ChatView, name = "chat"),
	path('login/', views.LoginPage, name = "login"),
	path('logout/', views.LogoutView, name = "logout"),
	path('register/', views.RegisterPage, name = "register"),
]
