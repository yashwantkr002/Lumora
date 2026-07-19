from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
)

from app.core.validators import (
    validate_image_size,
    validate_video_size,
)

from .user import CustomUser


class Story(
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
):
    """
    Instagram-style Story
    """

    IMAGE = "image"
    VIDEO = "video"

    MEDIA_TYPES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    ]

    PUBLIC = "public"
    FOLLOWERS = "followers"
    CLOSE_FRIENDS = "close_friends"

    PRIVACY_CHOICES = [
        (PUBLIC, "Public"),
        (FOLLOWERS, "Followers"),
        (CLOSE_FRIENDS, "Close Friends"),
    ]

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="stories",
    )

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
    )

    image = models.ImageField(
        upload_to="stories/images/",
        blank=True,
        null=True,
        validators=[validate_image_size],
    )

    video = models.FileField(
        upload_to="stories/videos/",
        blank=True,
        null=True,
        validators=[validate_video_size],
    )

    caption = models.CharField(
        max_length=250,
        blank=True,
    )

    privacy = models.CharField(
        max_length=20,
        choices=PRIVACY_CHOICES,
        default=FOLLOWERS,
    )

    expires_at = models.DateTimeField()

    views_count = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "stories"

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["privacy"]),
        ]

    def clean(self):

        super().clean()

        if self.media_type == self.IMAGE and not self.image:
            raise ValidationError(
                "Image is required."
            )

        if self.media_type == self.VIDEO and not self.video:
            raise ValidationError(
                "Video is required."
            )

        if self.image and self.video:
            raise ValidationError(
                "Story can contain only one media."
            )

    def save(self, *args, **kwargs):

        if not self.expires_at:
            self.expires_at = (
                timezone.now() + timedelta(hours=24)
            )

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.author.username}'s Story"