from django.contrib import admin
from . models import FriendRequest, PublicMessage

admin.site.register(PublicMessage)
admin.site.register(FriendRequest)
