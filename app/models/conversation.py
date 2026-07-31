from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
)

from .user import CustomUser


class Conversation(
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
):
    """
    Private / Group Conversation
    """

    PRIVATE = "private"
    GROUP = "group"

    CONVERSATION_TYPES = [
        (PRIVATE, "Private"),
        (GROUP, "Group"),
    ]

    conversation_type = models.CharField(
        max_length=20,
        choices=CONVERSATION_TYPES,
        default=PRIVATE,
    )

    title = models.CharField(
        max_length=120,
        blank=True,
    )

    participants = models.ManyToManyField(
        CustomUser,
        related_name="conversations",
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_conversations",
    )

    avatar = models.ImageField(
        upload_to="conversation/",
        blank=True,
        null=True,
    )

    last_message_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:

        db_table = "conversations"

        ordering = [
            "-last_message_at",
            "-created_at",
        ]

        indexes = [
            models.Index(fields=["conversation_type"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["last_message_at"]),
            models.Index(fields=["is_active"]),
        ]

    @property
    def participants_count(self):
        return self.participants.count()

    def __str__(self):
        if self.title:
            return self.title

        return f"Conversation {self.pk}"