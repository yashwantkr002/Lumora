"""
===========================================================
File: app/services/notification/query.py
===========================================================

PURPOSE

Provides optimized querysets for notifications.

Used by:

• NotificationCreateService
• NotificationReadService
• NotificationDeleteService

===========================================================
"""

from django.db.models import QuerySet

from app.models.notification import Notification


class NotificationQueryService:
    """
    Shared optimized querysets for notifications.
    """

    # -------------------------------------------------------
    # Base Queryset
    # -------------------------------------------------------

    @staticmethod
    def base_queryset() -> QuerySet[Notification]:
        """
        Base optimized queryset.
        """

        return (
            Notification.objects
            .select_related(
                "recipient",
                "recipient__profile",
                "actor",
                "actor__profile",
                "post",
                "comment",
            )
        )

    # -------------------------------------------------------
    # User Notifications
    # -------------------------------------------------------

    @staticmethod
    def user_queryset(
        *,
        user,
    ) -> QuerySet[Notification]:
        """
        Return notifications for a user.
        """

        return (
            NotificationQueryService
            .base_queryset()
            .filter(
                recipient=user,
            )
            .order_by(
                "-created_at",
            )
        )

    # -------------------------------------------------------
    # Unread Notifications
    # -------------------------------------------------------

    @staticmethod
    def unread_queryset(
        *,
        user,
    ) -> QuerySet[Notification]:
        """
        Return unread notifications.
        """

        return (
            NotificationQueryService
            .user_queryset(
                user=user,
            )
            .filter(
                is_read=False,
            )
        )

    # -------------------------------------------------------
    # Read Notifications
    # -------------------------------------------------------

    @staticmethod
    def read_queryset(
        *,
        user,
    ) -> QuerySet[Notification]:
        """
        Return read notifications.
        """

        return (
            NotificationQueryService
            .user_queryset(
                user=user,
            )
            .filter(
                is_read=True,
            )
        )

    # -------------------------------------------------------
    # Notification Count
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
            .unread_queryset(
                user=user,
            )
            .count()
        )

    # -------------------------------------------------------
    # Single Notification
    # -------------------------------------------------------

    @staticmethod
    def get_notification(
        *,
        notification_id,
    ) -> Notification | None:
        """
        Return a single notification.
        """

        return (
            NotificationQueryService
            .base_queryset()
            .filter(
                pk=notification_id,
            )
            .first()
        )