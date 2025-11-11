# apps/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from apps.auth_app.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        sender_id = data.get("sender_id")

        if not message or not sender_id:
            return

        sender = await User.objects.aget(id=sender_id)
        room = await ChatRoom.objects.aget(id=self.room_id)

        # Save message
        await Message.objects.acreate(room=room, sender=sender, content=message)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": str(sender.id),
                "sender_name": sender.name or sender.email,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_name": event["sender_name"],
        }))
