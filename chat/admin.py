from django.contrib import admin
from . models import FriendRequest, PublicMessage, PrivateChatRoom, PrivateMessage

admin.site.register(PublicMessage)
admin.site.register(FriendRequest)
admin.site.register(PrivateChatRoom)
admin.site.register(PrivateMessage)

