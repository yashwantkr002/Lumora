import logging

from django.shortcuts import get_object_or_404
from django.utils import timezone

from app.models.story import Story

logger = logging.getLogger(__name__)


class DetailStoryService:
    """
    Handles story retrieval.
    """

    @staticmethod
    def get_story(story_id: int) -> Story:
        """
        Return a single story.
        """

        story = get_object_or_404(
            Story.objects.select_related(
                "author",
                "author__profile",
            ),
            pk=story_id,
        )

        logger.info(
            "Story retrieved.",
            extra={
                "story_id": story.id,
            },
        )

        return story

    @staticmethod
    def get_active_stories():
        """
        Return all active stories.
        """

        return (
            Story.objects
            .select_related(
                "author",
                "author__profile",
            )
            .filter(
                expires_at__gt=timezone.now(),
            )
            .order_by("-created_at")
        )