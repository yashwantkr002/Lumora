"""
===========================================================
File: app/services/notification/delete.py
===========================================================

PURPOSE

Handles notification deletion.

===========================================================
"""

import logging

from django.core.exceptions import PermissionDenied
from django.db import transaction

from app.models.notification import Notification

from app.services.notification.query import (
    NotificationQueryService,
)

from app.services.notification.utils import (
    NotificationUtilsService,
)

logger = logging.getLogger(__name__)


class NotificationDeleteService:
    """
    Handles notification deletion.
    """

    # -------------------------------------------------------
    # Delete Notification
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def delete_notification(
        *,
        notification: Notification,
        user,
    ) -> None:
        """
        Delete a notification.
        """

        if notification.recipient != user:

            raise PermissionDenied(
                "You do not have permission to delete this notification."
            )

        notification_id = notification.id

        notification.delete()

        logger.info(
            "Notification deleted.",
            extra={
                "notification_id": notification_id,
                "user_id": user.id,
            },
        )

    # -------------------------------------------------------
    # Delete Read Notifications
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def delete_read_notifications(
        *,
        user,
    ) -> int:
        """
        Delete all read notifications.

        Returns:
            Number of deleted notifications.
        """

        deleted = (
            NotificationUtilsService
            .delete_read_notifications(
                user=user,
            )
        )

        logger.info(
            "Read notifications deleted.",
            extra={
                "user_id": user.id,
                "deleted": deleted,
            },
        )

        return deleted

    # -------------------------------------------------------
    # Delete All Notifications
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def delete_all_notifications(
        *,
        user,
    ) -> int:
        """
        Delete all notifications.

        Returns:
            Number of deleted notifications.
        """

        deleted, _ = (
            NotificationQueryService
            .user_queryset(
                user=user,
            )
            .delete()
        )

        logger.info(
            "All notifications deleted.",
            extra={
                "user_id": user.id,
                "deleted": deleted,
            },
        )

        return deleted