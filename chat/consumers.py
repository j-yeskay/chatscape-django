import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from . models import PublicMessage, Account


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


