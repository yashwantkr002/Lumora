"""
===========================================================
File: app/services/notification/utils.py
===========================================================

PURPOSE

Shared utility methods for notifications.

Used by:

• NotificationCreateService
• NotificationReadService
• NotificationDeleteService

===========================================================
"""

from django.db.models import F

from app.models.notification import Notification


class NotificationUtilsService:
    """
    Shared helper methods for notifications.
    """

    # -------------------------------------------------------
    # Mark As Read
    # -------------------------------------------------------

    @staticmethod
    def mark_as_read(
        *,
        notification: Notification,
    ) -> None:
        """
        Mark a notification as read.
        """

        if notification.is_read:

            return

        notification.is_read = True

        notification.save(
            update_fields=[
                "is_read",
            ],
        )

    # -------------------------------------------------------
    # Mark All As Read
    # -------------------------------------------------------

    @staticmethod
    def mark_all_as_read(
        *,
        user,
    ) -> int:
        """
        Mark all unread notifications as read.

        Returns:
            Number of updated notifications.
        """

        return (
            Notification.objects
            .filter(
                recipient=user,
                is_read=False,
            )
            .update(
                is_read=True,
            )
        )

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
            Notification.objects
            .filter(
                recipient=user,
                is_read=False,
            )
            .count()
        )

    # -------------------------------------------------------
    # Delete All Read
    # -------------------------------------------------------

    @staticmethod
    def delete_read_notifications(
        *,
        user,
    ) -> int:
        """
        Delete all read notifications.

        Returns:
            Number of deleted notifications.
        """

        deleted, _ = (
            Notification.objects
            .filter(
                recipient=user,
                is_read=True,
            )
            .delete()
        )

        return deleted