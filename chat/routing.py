from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/', consumers.PublicChatConsumer.as_asgi()),
    re_path(r'ws/privatechat/(?P<pk>\w+)/', consumers.PrivateChatConsumer.as_asgi())

]