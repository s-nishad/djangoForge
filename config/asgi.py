import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# 1️⃣ Set default Django settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')  # or 'config.prod' etc.

# 2️⃣ Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# 3️⃣ Import routing **after** Django is ready
from apps.chat.routing import websocket_urlpatterns

# 4️⃣ Define ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # for regular HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
