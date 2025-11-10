from django.urls import path
from .views import ChatRoomListCreateAPIView, MessageListCreateAPIView

app_name = "chat"

urlpatterns = [
    path("rooms/", ChatRoomListCreateAPIView.as_view(), name="chatroom-list-create"),
    path("rooms/<uuid:room_id>/messages/", MessageListCreateAPIView.as_view(), name="message-list-create"),
]
