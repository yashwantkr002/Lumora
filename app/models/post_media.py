"""
===========================================================
File: app/models/post_media.py
===========================================================

PURPOSE

Stores media attached to a post.

Supports:

• Multiple Images
• Multiple Videos
• Carousel
• Mixed Media

===========================================================
"""

from django.core.exceptions import ValidationError
from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from app.core.validators import (
    validate_image_size,
    validate_video_size,
)

from .post import Post


class PostMedia(
    UUIDModel,
    TimeStampedModel,
):
    """
    Media attached to a post.
    """

    # -------------------------------------------------------
    # Media Type
    # -------------------------------------------------------

    class MediaType(models.TextChoices):

        IMAGE = "image", "Image"

        VIDEO = "video", "Video"

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="media",
    )

    # -------------------------------------------------------
    # Media
    # -------------------------------------------------------

    media_type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
    )

    image = models.ImageField(
        upload_to="posts/images/%Y/%m/",
        blank=True,
        null=True,
        validators=[
            validate_image_size,
        ],
    )

    video = models.FileField(
        upload_to="posts/videos/%Y/%m/",
        blank=True,
        null=True,
        validators=[
            validate_video_size,
        ],
    )

    # -------------------------------------------------------
    # Future Ready
    # -------------------------------------------------------

    thumbnail = models.ImageField(
        upload_to="posts/thumbnails/%Y/%m/",
        blank=True,
        null=True,
    )

    duration = models.PositiveIntegerField(
        default=0,
        help_text="Video duration in seconds.",
    )

    order = models.PositiveSmallIntegerField(
        default=1,
        help_text="Carousel order.",
    )

    # -------------------------------------------------------
    # Meta
    # -------------------------------------------------------

    class Meta:

        db_table = "post_media"

        ordering = [
            "order",
            "created_at",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "post",
                    "order",
                ],
                name="unique_media_order_per_post",
            ),

        ]

        indexes = [

            models.Index(
                fields=[
                    "post",
                    "order",
                ]
            ),

            models.Index(
                fields=[
                    "media_type",
                ]
            ),

        ]

    # -------------------------------------------------------
    # Validation
    # -------------------------------------------------------

    def clean(self):

        super().clean()

        if (
            self.media_type == self.MediaType.IMAGE
            and not self.image
        ):

            raise ValidationError(
                "Image is required."
            )

        if (
            self.media_type == self.MediaType.VIDEO
            and not self.video
        ):

            raise ValidationError(
                "Video is required."
            )

        if self.image and self.video:

            raise ValidationError(
                "Only one media file is allowed."
            )

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------

    @property
    def file(self):
        """
        Returns the active media file.
        """

        if self.media_type == self.MediaType.IMAGE:

            return self.image

        return self.video

    @property
    def is_image(self) -> bool:

        return (
            self.media_type
            == self.MediaType.IMAGE
        )

    @property
    def is_video(self) -> bool:

        return (
            self.media_type
            == self.MediaType.VIDEO
        )

    # -------------------------------------------------------
    # String Representation
    # -------------------------------------------------------

    def __str__(self):

        return (
            f"{self.post.author.username} "
            f"- {self.media_type} "
            f"#{self.order}"
        )