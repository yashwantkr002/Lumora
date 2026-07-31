"""
===========================================================
File: app/services/notification/read.py
===========================================================

PURPOSE

Handles notification read operations.

===========================================================
"""

import logging

from django.db import transaction
from django.shortcuts import get_object_or_404

from app.models.notification import Notification

from app.services.notification.query import (
    NotificationQueryService,
)

from app.services.notification.utils import (
    NotificationUtilsService,
)

logger = logging.getLogger(__name__)


class NotificationReadService:
    """
    Handles notification read operations.
    """

    # -------------------------------------------------------
    # Get Notification
    # -------------------------------------------------------

    @staticmethod
    def get_notification(
        *,
        notification_id,
    ) -> Notification:
        """
        Return a notification.
        """

        return get_object_or_404(
            NotificationQueryService.base_queryset(),
            pk=notification_id,
        )

    # -------------------------------------------------------
    # Mark As Read
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def mark_as_read(
        *,
        notification: Notification,
    ) -> Notification:
        """
        Mark a notification as read.
        """

        NotificationUtilsService.mark_as_read(
            notification=notification,
        )

        logger.info(
            "Notification marked as read.",
            extra={
                "notification_id": notification.id,
            },
        )

        return notification

    # -------------------------------------------------------
    # Mark All As Read
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def mark_all_as_read(
        *,
        user,
    ) -> int:
        """
        Mark all notifications as read.

        Returns:
            Number of updated notifications.
        """

        updated = (
            NotificationUtilsService
            .mark_all_as_read(
                user=user,
            )
        )

        logger.info(
            "All notifications marked as read.",
            extra={
                "user_id": user.id,
                "updated": updated,
            },
        )

        return updated

    # -------------------------------------------------------
    # Unread Count
    # -------------------------------------------------------

    @staticmethod
    def unread_count(
        *,
        user,
    ) -> int:
        """
        Return unread notification count.
        """

        return (
            NotificationQueryService
            .unread_count(
                user=user,
            )
        )