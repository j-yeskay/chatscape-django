from .forms import ChangePasswordForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, EditDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from . models import Account, Message
from . msgs import SuccessMessageMixin




def IndexView(request):
	return render(request, 'chat/index.html', {})



def LoginPage(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(request, username = username, password = password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'Username or Password is wrong!')
			return redirect('login')

	return render(request, 'chat/login.html', {})


def LogoutView(request):
	logout(request)
	return redirect('login')


def RegisterPage(request):
	form = UserRegistrationForm()
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account Created Successfully! Login Now!')
			return redirect('login')
		
	return render(request, 'chat/register.html', {'form':form})


@login_required(login_url = 'index')
def HomeView(request):
	current_user_id = request.user.id
	current_user_account = Account.objects.filter(id = current_user_id)
	return render(request, 'chat/home.html', {'account_details':current_user_account})

@login_required(login_url = 'index')
def FindView(request):
	current_user_id = request.user.id
	all_except_current_user = Account.objects.exclude(id = current_user_id)
	
	if 'q' in request.GET:
		q = request.GET['q']
		search_results = all_except_current_user.filter(username__istartswith=q)
		return render(request, 'chat/find.html', {'search_results':search_results})
	else:
		return render(request, 'chat/find.html', {})

@login_required(login_url = 'index')
def AccountDetailView(request, pk):
	print(pk)
	account = Account.objects.filter(id=pk)
	print(account)
	return render(request, 'chat/accountdetails.html',{'accountdetail':account})


class EditDetailsView(SuccessMessageMixin, generic.UpdateView):
	form_class = EditDetailsForm
	template_name = 'chat/editdetails.html'
	success_url = reverse_lazy('home')
	success_message = "Details Edited Successfully!"

	def get_object(self):
		return self.request.user


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
	form_class = ChangePasswordForm 
	template_name = 'chat/changepassword.html'
	success_url = reverse_lazy('home')
	success_message = "Password Changed Successfully!"

@login_required(login_url = "index")
def ChatView(request):
	old_messages = Message.objects.all()
	return render(request, 'chat/chat.html', {
		'username': request.user.username,
		'old_messages': old_messages
	})
	