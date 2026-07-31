"""
===========================================================
File: app/models/view.py
===========================================================

PURPOSE

Stores post views.

Supports

• Anonymous Views
• Authenticated Views
• Analytics

===========================================================
"""

from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from .post import Post
from .user import CustomUser


class View(
    UUIDModel,
    TimeStampedModel,
):
    """
    Represents a post view.
    """

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="views",
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="views",
        null=True,
        blank=True,
    )

    # -------------------------------------------------------
    # Client Information
    # -------------------------------------------------------

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    class Meta:

        db_table = "views"

        ordering = [
            "-created_at",
        ]

        indexes = [

            models.Index(
                fields=[
                    "post",
                ],
            ),

            models.Index(
                fields=[
                    "user",
                ],
            ),

            models.Index(
                fields=[
                    "created_at",
                ],
            ),

        ]

    def __str__(self):

        if self.user:

            return (
                f"{self.user.username} "
                f"viewed {self.post.id}"
            )

        return (
            f"Anonymous viewed "
            f"{self.post.id}"
        )