from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from rest_framework.exceptions import ValidationError

User = get_user_model()

class ChatRoomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(user1=user) | ChatRoom.objects.filter(user2=user)

    def perform_create(self, serializer):
        user1 = self.request.user  # authenticated user
        user2_id = self.request.data.get("user2_id")

        if not user2_id:
            raise ValidationError({"user2_id": "This field is required."})

        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            raise ValidationError({"user2_id": "User does not exist."})

        room = ChatRoom.get_or_create_room(user1, user2)
        serializer.instance = room
        serializer.save()


class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        return Message.objects.filter(room_id=room_id).order_by("timestamp")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
