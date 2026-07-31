from typing import Any

from app.models.message import Message


class MessageSerializer:
    """Simple serializer for chat payloads and future WebSocket use."""

    @staticmethod
    def serialize(message: Message) -> dict[str, Any]:
        return {
            "id": str(message.id),
            "conversation_id": str(message.conversation_id),
            "sender_id": str(message.sender_id),
            "sender_name": message.sender.username,
            "content": message.content,
            "message_type": message.message_type,
            "created_at": message.created_at.isoformat(),
            "delivered": message.delivered,
            "seen": message.seen,
        }
