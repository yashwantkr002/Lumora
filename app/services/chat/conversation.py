import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models.conversation import Conversation

logger = logging.getLogger(__name__)


class ConversationService:
    """
    Handles conversation retrieval.
    """

    @staticmethod
    def get_user_conversations(user):
        """
        Return conversations for a user.
        """

        return (
            Conversation.objects.filter(
                participants=user,
            )
            .order_by(
                "-last_message_at",
                "-created_at",
            )
        )


@login_required
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