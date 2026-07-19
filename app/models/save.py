"""
===========================================================
File: app/models/save.py
===========================================================

PURPOSE

Stores bookmarked posts.

Bookmarks are private to the user.

===========================================================
"""

from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from .post import Post
from .user import CustomUser


class Save(
    UUIDModel,
    TimeStampedModel,
):
    """
    Represents a bookmarked post.
    """

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="saved_posts",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="saves",
    )

    class Meta:

        db_table = "saved_posts"

        ordering = [
            "-created_at",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "user",
                    "post",
                ],
                name="unique_saved_post",
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
            f"saved {self.post.id}"
        )