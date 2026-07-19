import logging

from django.shortcuts import get_object_or_404

from app.models.conversation import Conversation

logger = logging.getLogger(__name__)


class DetailConversationService:
    """
    Handles conversation retrieval.
    """

    @staticmethod
    def get_conversation(conversation_id: int) -> Conversation:
        """
        Return a conversation.
        """

        conversation = get_object_or_404(
            Conversation.objects.prefetch_related(
                "participants",
                "messages",
            ),
            pk=conversation_id,
        )

        logger.info(
            "Conversation retrieved.",
            extra={
                "conversation_id": conversation.id,
            },
        )

        return conversation