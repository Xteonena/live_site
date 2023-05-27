import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from ..live_app.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live.settings')
django_asgi_app = get_asgi_application()

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
