"""
===========================================================
File: app/services/follow/follow.py
===========================================================

PURPOSE

Handles follow relationships.

===========================================================
"""

import logging

from django.core.exceptions import PermissionDenied
from django.db import transaction

from app.models.follow import UserFollow
from app.models.notification import Notification
from app.models.user import CustomUser
from app.services.notification.create import NotificationCreateService

logger = logging.getLogger(__name__)


class FollowService:
    """
    Handles follow relationships.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Follow another user.
    #
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def follow_user(
        *,
        follower: CustomUser,
        following: CustomUser,
    ) -> UserFollow:
        """
        Create a follow relationship.
        """

        # -------------------------------------------------------
        # FIX #2
        #
        # Prevent users from following themselves.
        #
        # -------------------------------------------------------

        if follower == following:
            raise PermissionDenied(
                "You cannot follow yourself."
            )

        # -------------------------------------------------------
        # FIX #3
        #
        # Create follow relationship if it does not exist.
        #
        # -------------------------------------------------------

        follow_obj, created = UserFollow.objects.get_or_create(
            follower=follower,
            following=following,
        )
        if created:
            NotificationCreateService.create_notification(
                actor=follower,
                recipient=following,
                notification_type=Notification.NotificationType.FOLLOW,
            )
        # -------------------------------------------------------
        # FIX #4
        #
        # Log follow activity.
        #
        # -------------------------------------------------------

        logger.info(
            "Follow relationship %s.",
            "created" if created else "already exists",
            extra={
                "follower_id": follower.id,
                "following_id": following.id,
                "created": created,
            },
        )

        return follow_obj