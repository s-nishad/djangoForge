from rest_framework import serializers
from .models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    other_user_name = serializers.SerializerMethodField()
    class Meta:
        model = ChatRoom
        fields = ["id", "user1", "user2", "created_at", "other_user_name"]
        read_only_fields = ["id", "user1", "user2", "created_at"]

    def get_other_user_name(self, obj):
        user = self.context['request'].user
        if obj.user1 == user:
            return obj.user2.name or obj.user2.email
        return obj.user1.name or obj.user1.email

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'file', 'timestamp', 'sender_name']


    def get_sender_name(self, obj):
        return obj.sender.name or obj.sender.email
