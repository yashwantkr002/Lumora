from django.urls import path

from app.views.chat.conversations import conversations
from app.services.chat.message import messages_view
from app.services.chat.websocket import websocket_info

urlpatterns = [
    path(
        "",
        conversations,
        name="conversations",
    ),
    path(
        "<int:conversation_id>/",
        messages_view,
        name="messages",
    ),
    path(
        "websocket/",
        websocket_info,
        name="websocket",
    ),
]