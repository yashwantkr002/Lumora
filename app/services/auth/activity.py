"""
===========================================================
File: app/services/auth/activity.py
===========================================================

PURPOSE

Handles user activity.

Only this service should update UserActivity.

===========================================================
"""

import logging

from django.utils import timezone

from app.models.user import UserActivity

logger = logging.getLogger(__name__)


class ActivityService:
    """
    Handles user online/offline activity.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Get or create activity record.
    #
    # Prevents RelatedObjectDoesNotExist errors.
    #
    # -------------------------------------------------------

    @staticmethod
    def get_activity(user) -> UserActivity:

        activity, _ = UserActivity.objects.get_or_create(
            user=user,
        )

        return activity

    # -------------------------------------------------------
    # FIX #2
    #
    # Mark user online.
    #
    # -------------------------------------------------------

    @staticmethod
    def mark_online(user) -> None:

        activity = ActivityService.get_activity(user)

        activity.is_online = True
        activity.last_seen = timezone.now()

        activity.save(
            update_fields=[
                "is_online",
                "last_seen",
            ]
        )

        logger.info(
            "User marked online.",
            extra={
                "user_id": user.id,
            },
        )

    # -------------------------------------------------------
    # FIX #3
    #
    # Mark user offline.
    #
    # -------------------------------------------------------

    @staticmethod
    def mark_offline(user) -> None:

        activity = ActivityService.get_activity(user)

        activity.is_online = False
        activity.last_seen = timezone.now()

        activity.save(
            update_fields=[
                "is_online",
                "last_seen",
            ]
        )

        logger.info(
            "User marked offline.",
            extra={
                "user_id": user.id,
            },
        )

    # -------------------------------------------------------
    # FIX #4
    #
    # Update only last seen.
    #
    # Useful for middleware, APIs and WebSockets.
    #
    # -------------------------------------------------------

    @staticmethod
    def update_last_seen(user) -> None:

        activity = ActivityService.get_activity(user)

        activity.last_seen = timezone.now()

        activity.save(
            update_fields=[
                "last_seen",
            ]
        )

        logger.info(
            "Last seen updated.",
            extra={
                "user_id": user.id,
            },
        )