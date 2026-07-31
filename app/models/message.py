from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
)

from app.core.validators import (
    validate_image_size,
    validate_video_size,
)

from .conversation import Conversation
from .user import CustomUser


class Message(
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
):
    """
    Instagram / WhatsApp style message model.
    """

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"
    AUDIO = "audio"

    MESSAGE_TYPES = [
        (TEXT, "Text"),
        (IMAGE, "Image"),
        (VIDEO, "Video"),
        (FILE, "File"),
        (AUDIO, "Audio"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    reply_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replies",
    )

    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default=TEXT,
    )

    content = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="messages/images/",
        null=True,
        blank=True,
        validators=[validate_image_size],
    )

    video = models.FileField(
        upload_to="messages/videos/",
        null=True,
        blank=True,
        validators=[validate_video_size],
    )

    attachment = models.FileField(
        upload_to="messages/files/",
        null=True,
        blank=True,
    )

    audio = models.FileField(
        upload_to="messages/audio/",
        null=True,
        blank=True,
    )

    is_edited = models.BooleanField(
        default=False,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    delivered = models.BooleanField(
        default=False,
    )

    seen = models.BooleanField(
        default=False,
    )

    seen_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:

        db_table = "messages"

        ordering = [
            "created_at",
        ]

        indexes = [
            models.Index(fields=["conversation"]),
            models.Index(fields=["sender"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["seen"]),
            models.Index(fields=["delivered"]),
        ]

    def save(self, *args, **kwargs):

        if self.pk:
            self.is_edited = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender.username} → {self.conversation.id}"