"""
===========================================================
File: app/models/like.py
===========================================================

PURPOSE

Stores likes for posts.

===========================================================
"""

from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from .post import Post
from .user import CustomUser


class Like(
    UUIDModel,
    TimeStampedModel,
):
    """
    Represents a user's like on a post.
    """

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:

        db_table = "likes"

        ordering = [
            "-created_at",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "user",
                    "post",
                ],
                name="unique_post_like",
            ),

        ]

        indexes = [

            models.Index(
                fields=["user"],
            ),

            models.Index(
                fields=["post"],
            ),

            models.Index(
                fields=["created_at"],
            ),

        ]

    def __str__(self):

        return (
            f"{self.user.username} "
            f"liked {self.post.id}"
        )