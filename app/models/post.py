"""
===========================================================
File: app/models/post.py
===========================================================

PURPOSE

Core Post model.

Stores post-level information only.

Media files are stored in PostMedia.

===========================================================
"""

from django.db import models

from app.core.models import (
    UUIDModel,
    SoftDeleteModel,
    TimeStampedModel,
)

from .tag import Tag
from .user import CustomUser


class Post(
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
):
    """
    Social media post.

    Contains only post metadata.

    Media is stored in PostMedia.
    """

    # -------------------------------------------------------
    # Visibility
    # -------------------------------------------------------

    class Visibility(models.TextChoices):

        PUBLIC = "public", "Public"

        FOLLOWERS = "followers", "Followers"

        PRIVATE = "private", "Private"

    # -------------------------------------------------------
    # Author
    # -------------------------------------------------------

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    # -------------------------------------------------------
    # Content
    # -------------------------------------------------------

    caption = models.TextField(
        max_length=2200,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts",
    )

    # -------------------------------------------------------
    # Privacy
    # -------------------------------------------------------

    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
        db_index=True,
    )

    allow_comments = models.BooleanField(
        default=True,
    )

    allow_download = models.BooleanField(
        default=False,
    )

    # -------------------------------------------------------
    # Analytics
    # -------------------------------------------------------

    views_count = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    likes_count = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    comments_count = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    shares_count = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    saves_count = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    class Meta:

        db_table = "posts"

        ordering = [
            "-created_at",
        ]

        indexes = [

            # Feed

            models.Index(
                fields=[
                    "author",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "visibility",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "-likes_count",
                ]
            ),

            models.Index(
                fields=[
                    "-views_count",
                ]
            ),


        ]
        constraints = [

            models.CheckConstraint(
                condition=models.Q(
                    likes_count__gte=0,
                ),
                name="post_likes_count_positive",
            ),

            models.CheckConstraint(
                condition=models.Q(
                    comments_count__gte=0,
                ),
                name="post_comments_count_positive",
            ),

            models.CheckConstraint(
                condition=models.Q(
                    shares_count__gte=0,
                ),
                name="post_shares_count_positive",
            ),

            models.CheckConstraint(
                condition=models.Q(
                    saves_count__gte=0,
                ),
                name="post_saves_count_positive",
            ),

            models.CheckConstraint(
                condition=models.Q(
                    views_count__gte=0,
                ),
                name="post_views_count_positive",
            ),
        ]

    # -------------------------------------------------------
    # Computed Properties
    # -------------------------------------------------------

    @property
    def engagement_score(self) -> int:
        """
        Total engagement score.
        """

        return (
            self.likes_count
            + self.comments_count
            + self.shares_count
            + self.saves_count
        )

    @property
    def media_count(self) -> int:
        """
        Total attached media.
        """

        return self.media.count()

    # -------------------------------------------------------
    # String Representation
    # -------------------------------------------------------

    def __str__(self) -> str:

        return (
            f"Post("
            f"{self.author.username}, "
            f"{self.created_at:%Y-%m-%d}"
            f")"
        )
