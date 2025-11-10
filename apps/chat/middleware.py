from urllib.parse import parse_qs
from channels.middleware.base import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import jwt

User = get_user_model()


@database_sync_to_async
def get_user(token):
    try:
        UntypedToken(token)  # validate token
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")
        return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, jwt.ExpiredSignatureError, User.DoesNotExist):
        return None


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate user via JWT token in query string
    ws://.../ws/chat/<user_id>/?token=<JWT>
    """

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        qs = parse_qs(query_string)
        token = qs.get("token")
        scope["user"] = await get_user(token[0]) if token else None
        return await super().__call__(scope, receive, send)
