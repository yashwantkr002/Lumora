import logging

from django.core.exceptions import PermissionDenied
from django.db import transaction

from app.models.story import Story

logger = logging.getLogger(__name__)


class DeleteStoryService:
    """
    Handles story deletion.
    """

    @staticmethod
    @transaction.atomic
    def delete_story(
        *,
        story: Story,
        user,
    ) -> bool:
        """
        Delete a story.
        """

        if story.user != user:
            raise PermissionDenied(
                "You are not allowed to delete this story."
            )

        story_id = story.id

        story.delete()

        logger.info(
            "Story deleted.",
            extra={
                "story_id": story_id,
                "user_id": user.id,
            },
        )

        return True