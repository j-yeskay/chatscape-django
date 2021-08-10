from .forms import ChangePasswordForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, EditDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from . models import Account, PublicMessage, FriendRequest
from . msgs import SuccessMessageMixin




def get_no_of_friend_requests(req):
	current_account = Account.objects.get(username = req.user)
	my_requests = FriendRequest.objects.filter(receiver_account = current_account)
	return len(my_requests)



def IndexView(request):
	if request.user.is_authenticated:
		return redirect("home")
	else:
		return render(request, 'chat/index.html', {})



def LoginPage(request):
	if request.user.is_authenticated:
		return redirect("home")
	else:
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
	return render(request, 'chat/home.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'account_details':current_user_account})

@login_required(login_url = 'index')
def FindView(request):
	current_user_id = request.user.id
	all_except_current_user = Account.objects.exclude(id = current_user_id)
	
	if 'q' in request.GET:
		q = request.GET['q']
		search_results = all_except_current_user.filter(username__istartswith=q)
		return render(request, 'chat/find.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'search_results':search_results})
	else:
		return render(request, 'chat/find.html', {'no_of_friend_requests': get_no_of_friend_requests(request)})

@login_required(login_url = 'index')
def AccountDetailView(request, pk):
	account = Account.objects.filter(id=pk)
	already_friend = 0
	already_got_friend_request = 0
	if request.user == (Account.objects.get(pk = pk)):
		return redirect("home")
	
	current_account = Account.objects.get(username = request.user)
	current_friends = current_account.friends.all()
	for friend in current_friends:
		if friend == (Account.objects.get(pk = pk)):
			already_friend = 1
	try:
		f_req = FriendRequest.objects.get(sender_account = Account.objects.get(pk = pk), receiver_account = request.user)
		requestid = f_req.id
		already_got_friend_request = 1
	except FriendRequest.DoesNotExist:
		f_req = None
		requestid = None	
		
	return render(request, 'chat/accountdetails.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'accountdetail':account, 'already_friend':already_friend, 'already_got_friend_request':already_got_friend_request, 'friendid':pk, 'requestid':requestid})


class EditDetailsView(SuccessMessageMixin, generic.UpdateView):
	form_class = EditDetailsForm
	template_name = 'chat/editdetails.html'
	success_url = reverse_lazy('home')
	success_message = "Details Edited Successfully!"
	
	def get_object(self):
		return self.request.user

	def get_context_data(self, **kwargs):
		context =  super().get_context_data(**kwargs)
		context['no_of_friend_requests'] = get_no_of_friend_requests(self.request)
		return context


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
	form_class = ChangePasswordForm 
	template_name = 'chat/changepassword.html'
	success_url = reverse_lazy('home')
	success_message = "Password Changed Successfully!"

	def get_context_data(self, **kwargs):
		context =  super().get_context_data(**kwargs)
		context['no_of_friend_requests'] = get_no_of_friend_requests(self.request)
		return context


@login_required(login_url = "index")
def SendFriendRequestView(request, pk):
	sender_account = Account.objects.get(username = request.user)
	receiver_account = Account.objects.get(id = pk)

	if sender_account.id == receiver_account.id:
		return redirect('home')

	friend_request, created = FriendRequest.objects.get_or_create(sender_account = sender_account, receiver_account = receiver_account)

	if created:
		messages.success(request,"Friend Request Sent!")
		return redirect('accountdetails', pk = pk)

	else:
		messages.error(request,"Friend Request ALREADY Sent!")
		return redirect('accountdetails', pk = pk)

@login_required(login_url = "index")
def MyRequestsView(request):
	current_account = Account.objects.get(username = request.user)
	my_requests = FriendRequest.objects.filter(receiver_account = current_account)
	return render(request,'chat/myrequests.html', {'no_of_friend_requests': get_no_of_friend_requests(request),'my_requests':my_requests})


@login_required(login_url = "index")
def MyFriendsView(request):
	current_account = Account.objects.get(username = request.user)
	my_friends = current_account.friends.all()
	no_of_friends = len(my_friends)
	return render(request,'chat/myfriends.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'my_friends':my_friends, 'no_of_friends':no_of_friends})

@login_required(login_url = "index")
def AcceptFriendRequestView(request, pk):
	friend_request = FriendRequest.objects.get(id = pk)

	if friend_request.receiver_account == request.user:
		friend_request.receiver_account.friends.add(friend_request.sender_account)
		friend_request.sender_account.friends.add(friend_request.receiver_account)

		friend_request.delete()
		messages.success(request,"Friend Request Accepted!")
		return redirect('myrequests')
	else:
		return redirect("home")


@login_required(login_url = "index")
def UnfriendView(request, pk):
	current_account = Account.objects.get(username = request.user)
	friend_account = Account.objects.get(id = pk)
	current_account.friends.remove(friend_account)
	friend_account.friends.remove(current_account)
	messages.error(request,"Friend Removed!")
	return redirect('myfriends')


@login_required(login_url = "index")
def ChatView(request):
	old_messages = PublicMessage.objects.all()
	return render(request, 'chat/chat.html', {
		'no_of_friend_requests': get_no_of_friend_requests(request),
		'username': request.user.username,
		'old_messages': old_messages
	})
	