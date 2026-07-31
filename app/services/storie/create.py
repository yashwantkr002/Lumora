import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from app.models.story import Story

logger = logging.getLogger(__name__)


class CreateStoryService:
    """
    Handles story creation.
    """

    STORY_DURATION = timedelta(hours=24)

    @staticmethod
    @transaction.atomic
    def create_story(
        *,
        user,
        cleaned_data,
        files,
    ) -> Story:
        """
        Create a new story.
        """

        story = Story.objects.create(
            user=user,
            expires_at=timezone.now() + CreateStoryService.STORY_DURATION,
        )

        if files.get("image"):
            story.image = files["image"]

        if files.get("video"):
            story.video = files["video"]

        story.full_clean()

        story.save()

        logger.info(
            "Story created.",
            extra={
                "story_id": story.id,
                "user_id": user.id,
            },
        )

        return story