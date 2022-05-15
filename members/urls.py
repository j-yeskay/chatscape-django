from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name="login"),
    path('logout/', views.LogoutView, name="logout"),
    path('register/', views.RegisterPage, name="register"),
    path('editdetails/', login_required(views.EditDetailsView.as_view(), login_url="home"), name="editdetails"),
    path('password/', login_required(views.ChangePasswordView.as_view(), login_url="home"), name="changepassword"),
]
