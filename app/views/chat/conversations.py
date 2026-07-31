
import logging  
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

from app.services.chat.conversation import ConversationService


def conversations(request):
    """
    Display all conversations for the current user.
    """

    try:

        user_conversations = (
            ConversationService.get_user_conversations(
                request.user,
            )
        )

        logger.info(
            "Conversation list loaded.",
            extra={
                "user_id": request.user.id,
            },
        )

    except Exception:

        logger.exception(
            "Unable to load conversations.",
            extra={
                "user_id": request.user.id,
            },
        )

        user_conversations = []

    return render(
        request,
        "chat/conversations.html",
        {
            "conversations": user_conversations,
        },
    )