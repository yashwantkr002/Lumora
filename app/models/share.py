"""
===========================================================
File: app/models/share.py
===========================================================

PURPOSE

Stores repost/share history.

Supports

• One share per user per post
• Share counter
• Future repost timeline

===========================================================
"""

from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from .post import Post
from .user import CustomUser


class Share(
    UUIDModel,
    TimeStampedModel,
):
    """
    Represents a shared post.
    """

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="shares",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="shares",
    )

    class Meta:

        db_table = "shares"

        ordering = [
            "-created_at",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "user",
                    "post",
                ],
                name="unique_post_share",
            ),

        ]

        indexes = [

            models.Index(
                fields=[
                    "user",
                ],
            ),

            models.Index(
                fields=[
                    "post",
                ],
            ),

            models.Index(
                fields=[
                    "created_at",
                ],
            ),

        ]

    def __str__(self):

        return (
            f"{self.user.username} "
            f"shared {self.post.id}"
        )