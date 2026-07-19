from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from .story import Story
from .user import CustomUser


class StoryView(
    UUIDModel,
    TimeStampedModel,
):

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="story_views",
    )

    viewer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="viewed_stories",
    )

    class Meta:

        db_table = "story_views"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "story",
                    "viewer",
                ],
                name="unique_story_view",
            )
        ]

        indexes = [
            models.Index(fields=["story"]),
            models.Index(fields=["viewer"]),
        ]

    def __str__(self):
        return f"{self.viewer} viewed {self.story}"