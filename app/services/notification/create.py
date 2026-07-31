"""
===========================================================
File: app/services/notification/create.py
===========================================================

PURPOSE

Handles notification creation.

===========================================================
"""

import logging

from django.db import transaction

from app.models.comment import Comment
from app.models.notification import Notification
from app.models.post import Post
from app.models.user import CustomUser

logger = logging.getLogger(__name__)


class NotificationCreateService:
    """
    Handles notification creation.
    """

    @staticmethod
    @transaction.atomic
    def create_notification(
        *,
        recipient: CustomUser,
        actor: CustomUser,
        notification_type: str,
        post: Post | None = None,
        comment: Comment | None = None,
    ) -> Notification | None:
        """
        Create a notification.

        Returns:
            Notification | None
        """

        # -------------------------------------------------------
        # Prevent Self Notifications
        # -------------------------------------------------------

        if recipient == actor:

            return None

        # -------------------------------------------------------
        # Create Notification
        # -------------------------------------------------------

        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            notification_type=notification_type,
            post=post,
            comment=comment,
        )

        logger.info(
            "Notification created.",
            extra={
                "notification_id": notification.id,
                "recipient_id": recipient.id,
                "actor_id": actor.id,
                "type": notification_type,
            },
        )

        return notification