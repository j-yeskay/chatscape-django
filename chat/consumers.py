import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from . models import PrivateChatRoom, PublicMessage, PrivateMessage
from members.models import Account


class PublicChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = ''
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message_content']
        sender_username = data['sender_username']

        await self.save_message(sender_username, message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                    'sender_username': sender_username,
                    'message_content': message_content
            }
        )

    async def chat_message(self, event):
        message_content = event['message_content']
        sender_username = event['sender_username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender_username': sender_username,
            'message_content': message_content

        }))

    @sync_to_async
    def save_message(self, sender_username, message_content):
        sender = Account.objects.get(username = sender_username)
        PublicMessage.objects.create(sender = sender, message_content = message_content)


class PrivateChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat_room = data['chat_room']
        message_content = data['message_content']
        sender_username = data['sender_username']

        await self.save_message(chat_room, sender_username, message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                    'chat_room' : chat_room,
                    'sender_username': sender_username,
                    'message_content': message_content
            }
        )

    async def chat_message(self, event):
        chat_room = event['chat_room']
        message_content = event['message_content']
        sender_username = event['sender_username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'chat_room' : chat_room,
            'sender_username' : sender_username,
            'message_content' : message_content

        }))

    @sync_to_async
    def save_message(self, chat_room, sender_username, message_content):
        sender = Account.objects.get(username = sender_username)
        chat_room = PrivateChatRoom.objects.get(id = chat_room)
        PrivateMessage.objects.create(chat_room = chat_room, sender = sender, message_content = message_content)
    




