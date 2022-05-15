from .forms import ChangePasswordForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, EditDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from . models import Account
from chat.models import PublicMessage, FriendRequest
from . msgs import SuccessMessageMixin
from chat.views import get_no_of_friend_requests

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or Password is wrong!')
                return redirect('login')
    return render(request, 'members/login.html', {})


def LogoutView(request):
    logout(request)
    return redirect('login')


def RegisterPage(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Account Created Successfully! Login Now!')
            return redirect('login')

    return render(request, 'members/register.html', {'form': form})


class EditDetailsView(SuccessMessageMixin, generic.UpdateView):
    form_class = EditDetailsForm
    template_name = 'members/editdetails.html'
    success_url = reverse_lazy('home')
    success_message = "Details Edited Successfully!"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_of_friend_requests'] = get_no_of_friend_requests(
            self.request)
        return context


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'members/changepassword.html'
    success_url = reverse_lazy('home')
    success_message = "Password Changed Successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_of_friend_requests'] = get_no_of_friend_requests(
            self.request)
        return context