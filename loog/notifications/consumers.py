import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['session']['_auth_user_id']
        self.room_name = str(self.user_id)
        self.room_group_name = 'chat_%s' % self.room_name      

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def notification_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
    
    async def system_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
