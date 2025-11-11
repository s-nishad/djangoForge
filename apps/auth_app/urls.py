from django.urls import path
from .views import UserListAPIView

app_name = "auth_app"

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
]
