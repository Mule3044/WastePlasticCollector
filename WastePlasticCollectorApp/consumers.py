
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'user_{self.user_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            # Parse the incoming text_data as JSON
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')

            # Echo the received message back
            await self.send(text_data=json.dumps({'message': f"Received: {message}"}))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON received'}))

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
