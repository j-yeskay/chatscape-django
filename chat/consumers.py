import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from . models import PublicMessage


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
		message = data['message']
		sender = data['username']

		await self.save_message(sender, message)

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'username': sender,
				'message': message
			}
		)

	async def chat_message(self, event):
			message = event['message']
			sender = event['username']

			# Send message to WebSocket
			await self.send(text_data=json.dumps({
				'username': sender,
				'message': message
				
			}))

	@sync_to_async
	def save_message(self, sender, message):
		PublicMessage.objects.create(sender = sender, content=message)