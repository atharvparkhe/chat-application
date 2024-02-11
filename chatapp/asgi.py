import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from app_chats.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

application = get_asgi_application()

ws_patterns = [
    # path("ws/<room_id>/chat/<user_id>/" , ChatConsumer.as_asgi()),
    # path("ws/<room_id>/chat/" , ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket" : URLRouter(ws_patterns)
})