import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from apps.core.utils import uuid_factory

class ChatRoom(models.Model):
    id = models.CharField(max_length=255, default=uuid_factory, editable=False, primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_or_create_room(user1, user2):
        room = ChatRoom.objects.filter(
            models.Q(user1=user1, user2=user2) | models.Q(user1=user2, user2=user1)
        ).first()
        if not room:
            room = ChatRoom.objects.create(user1=user1, user2=user2)
        return room

    def __str__(self):
        return f"Room between {self.user1} and {self.user2}"


class Message(models.Model):
    id = models.UUIDField(max_length=255, primary_key=True, default=uuid_factory, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.content[:20]}"
