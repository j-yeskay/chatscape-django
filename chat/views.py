from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from members.models import Account
from . models import PrivateMessage, PublicMessage, FriendRequest, PrivateChatRoom


def get_no_of_friend_requests(req):
    current_account = Account.objects.get(username=req.user)
    my_requests = FriendRequest.objects.filter(
        receiver_account=current_account)
    return len(my_requests)


def IndexView(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request, 'chat/index.html', {})

@login_required(login_url='index')
def HomeView(request):
    current_user_id = request.user.id
    current_user_account = Account.objects.filter(id=current_user_id)
    return render(request, 'chat/home.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'account_details': current_user_account})


@login_required(login_url='index')
def FindView(request):
    current_user_id = request.user.id
    all_except_current_user = Account.objects.exclude(id=current_user_id)

    if 'q' in request.GET:
        q = request.GET['q']
        search_results = all_except_current_user.filter(
            username__istartswith=q)
        return render(request, 'chat/find.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'search_results': search_results})
    else:
        return render(request, 'chat/find.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'all_except_current_user': all_except_current_user})


@login_required(login_url='index')
def AccountDetailView(request, pk):
    account = Account.objects.filter(id=pk)
    already_friend = 0
    already_got_friend_request = 0
    if request.user == (Account.objects.get(pk=pk)):
        return redirect("home")

    current_account = Account.objects.get(username=request.user)
    current_friends = current_account.friends.all()
    for friend in current_friends:
        if friend == (Account.objects.get(pk=pk)):
            already_friend = 1
    try:
        f_req = FriendRequest.objects.get(
            sender_account=Account.objects.get(pk=pk), receiver_account=request.user)
        requestid = f_req.id
        already_got_friend_request = 1
    except FriendRequest.DoesNotExist:
        f_req = None
        requestid = None

    return render(request, 'chat/accountdetails.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'accountdetail': account, 'already_friend': already_friend, 'already_got_friend_request': already_got_friend_request, 'friendid': pk, 'requestid': requestid})


@login_required(login_url="index")
def SendFriendRequestView(request, pk):
    sender_account = Account.objects.get(username=request.user)
    receiver_account = Account.objects.get(id=pk)

    if sender_account.id == receiver_account.id:
        return redirect('home')

    friend_request, created = FriendRequest.objects.get_or_create(
        sender_account=sender_account, receiver_account=receiver_account)

    if created:
        messages.success(request, "Friend Request Sent!")
        return redirect('accountdetails', pk=pk)

    else:
        messages.error(request, "Friend Request ALREADY Sent!")
        return redirect('accountdetails', pk=pk)


@login_required(login_url="index")
def MyRequestsView(request):
    current_account = Account.objects.get(username=request.user)
    my_requests = FriendRequest.objects.filter(
        receiver_account=current_account)
    return render(request, 'chat/myrequests.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'my_requests': my_requests})


@login_required(login_url="index")
def MyFriendsView(request):
    current_account = Account.objects.get(username=request.user)
    my_friends = current_account.friends.all()
    private_chatroom_ids = {}

    for friend in my_friends:
        room_id = get_private_chatroom(request.user, friend)
        private_chatroom_ids[str(room_id)] = room_id
    
    friends_and_chatrooms = zip(list(my_friends), list(private_chatroom_ids))

    no_of_friends = len(my_friends)
    return render(request, 'chat/myfriends.html', {'no_of_friend_requests': get_no_of_friend_requests(request), 'my_friends': my_friends, 'no_of_friends': no_of_friends, 'friends_and_chatrooms' : friends_and_chatrooms})


def get_private_chatroom(account1, account2):
    try:
        chat_room = PrivateChatRoom.objects.get(account1 = account1, account2 = account2)
    except PrivateChatRoom.DoesNotExist:
        chat_room = PrivateChatRoom.objects.get(account1 = account2, account2 = account1)

    return chat_room.id


def create_private_chatroom(account1, account2):
    chatroom = PrivateChatRoom(account1 = account1, account2 = account2)
    chatroom.save()


def delete_private_chatroom(account1, account2):
    try:
        chat_room = PrivateChatRoom.objects.get(account1 = account1, account2 = account2)
        chat_room.delete()
    except PrivateChatRoom.DoesNotExist:
        chat_room = PrivateChatRoom.objects.get(account1 = account2, account2 = account1)
        chat_room.delete()
    



@login_required(login_url="index")
def AcceptFriendRequestView(request, pk):
    friend_request = FriendRequest.objects.get(id=pk)

    if friend_request.receiver_account == request.user:
        friend_request.receiver_account.friends.add(
            friend_request.sender_account)
        friend_request.sender_account.friends.add(
            friend_request.receiver_account)

        create_private_chatroom(friend_request.sender_account, friend_request.receiver_account)

        friend_request.delete()
        messages.success(request, "Friend Request Accepted!")
        return redirect('myrequests')
    else:
        return redirect("home")


@login_required(login_url="index")
def UnfriendView(request, pk):
    current_account = Account.objects.get(username=request.user)
    friend_account = Account.objects.get(id=pk)
    current_account.friends.remove(friend_account)
    friend_account.friends.remove(current_account)

    delete_private_chatroom(current_account, friend_account)
    
    messages.error(request, "Friend Removed!")
    return redirect('myfriends')


@login_required(login_url="index")
def PublicChatView(request):
    old_messages = PublicMessage.objects.all()
    return render(request, 'chat/publicchat.html', {
        'no_of_friend_requests': get_no_of_friend_requests(request),
        'username': request.user.username,
        'old_messages': old_messages
    })


@login_required(login_url="index")
def PrivateChatView(request, pk):
    chat_room = PrivateChatRoom.objects.get(id = pk)
    private_messages = PrivateMessage.objects.filter(chat_room = chat_room)
    
    return render(request, 'chat/privatechat.html', {
        'no_of_friend_requests': get_no_of_friend_requests(request),
        'username' : request.user.username,
        'chat_room' : chat_room,
        'private_messages' : private_messages,
    })
