"""
===========================================================
File: app/models/notification.py
===========================================================

PURPOSE

Stores user notifications.

===========================================================
"""

from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from .comment import Comment
from .post import Post
from .user import CustomUser


class Notification(
    UUIDModel,
    TimeStampedModel,
):
    """
    Represents a user notification.
    """

    # -------------------------------------------------------
    # Notification Types
    # -------------------------------------------------------

    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"
    REPLY = "reply"
    MENTION = "mention"

    NOTIFICATION_TYPES = [

        (LIKE, "Like"),

        (COMMENT, "Comment"),

        (FOLLOW, "Follow"),

        (REPLY, "Reply"),

        (MENTION, "Mention"),

    ]

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    actor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
        blank=True,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )

    # -------------------------------------------------------
    # Data
    # -------------------------------------------------------

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
    )

    is_read = models.BooleanField(
        default=False,
    )

    class Meta:

        db_table = "notifications"

        ordering = [
            "-created_at",
        ]

        indexes = [

            models.Index(
                fields=[
                    "recipient",
                ],
            ),

            models.Index(
                fields=[
                    "actor",
                ],
            ),

            models.Index(
                fields=[
                    "notification_type",
                ],
            ),

            models.Index(
                fields=[
                    "is_read",
                ],
            ),

            models.Index(
                fields=[
                    "created_at",
                ],
            ),

        ]

    def __str__(self):

        actor_name = self.actor.username if self.actor else "System"
        recipient_name = self.recipient.username if self.recipient else "Unknown"

        return (
            f"{actor_name} "
            f"{self.notification_type} "
            f"{recipient_name}"
        )