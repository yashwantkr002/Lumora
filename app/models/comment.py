from django.db import models
from django.core.exceptions import ValidationError

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
)

from .post import Post
from .user import CustomUser


class Comment(
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
):
    """
    Represents a comment on a post.

    Supports:

    • Nested replies
    • Soft delete
    • Like counter
    • Reply counter
    • Moderation
    """

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    # -------------------------------------------------------
    # Content
    # -------------------------------------------------------

    content = models.TextField(
        max_length=1000,
    )

    # -------------------------------------------------------
    # Status
    # -------------------------------------------------------

    is_edited = models.BooleanField(
        default=False,
    )

    is_pinned = models.BooleanField(
        default=False,
    )

    is_hidden = models.BooleanField(
        default=False,
    )

    # -------------------------------------------------------
    # Analytics
    # -------------------------------------------------------

    likes_count = models.PositiveIntegerField(
        default=0,
    )

    replies_count = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        db_table = "comments"

        ordering = [
            "created_at",
        ]

        indexes = [

            models.Index(
                fields=["post"],
            ),

            models.Index(
                fields=["author"],
            ),

            models.Index(
                fields=["parent"],
            ),

            models.Index(
                fields=["created_at"],
            ),

            models.Index(
                fields=["is_hidden"],
            ),

            models.Index(
                fields=["is_pinned"],
            ),

        ]

        constraints = [

            models.CheckConstraint(
                condition=~models.Q(
                    parent=models.F("id"),
                ),
                name="prevent_self_parent",
            ),

        ]

    # -------------------------------------------------------
    # Validation
    # -------------------------------------------------------

    def clean(self):

        super().clean()

        if self.parent:

            if self.parent == self:

                raise ValidationError(
                    "A comment cannot reply to itself."
                )

            if self.parent.post_id != self.post_id:

                raise ValidationError(
                    "Replies must belong to the same post."
                )

    # -------------------------------------------------------
    # String Representation
    # -------------------------------------------------------

    def __str__(self):

        return (
            f"{self.author.username} "
            f"commented on {self.post.id}"
        )