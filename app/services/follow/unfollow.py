"""
===========================================================
File: app/services/follow/unfollow.py
===========================================================

PURPOSE

Handles unfollow relationships.

===========================================================
"""

import logging

from django.db import transaction

from app.models.follow import UserFollow
from app.models.user import CustomUser

logger = logging.getLogger(__name__)


class UnfollowService:
    """
    Handles unfollow relationships.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Remove follow relationship.
    #
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def unfollow_user(
        *,
        follower: CustomUser,
        following: CustomUser,
    ) -> bool:
        """
        Remove an existing follow relationship.
        """

        relationship = UserFollow.objects.filter(
            follower=follower,
            following=following,
        )

        if relationship.exists():

            relationship.delete()

            logger.info(
                "Follow relationship removed.",
                extra={
                    "follower_id": follower.id,
                    "following_id": following.id,
                },
            )

            return True

        logger.info(
            "Follow relationship does not exist.",
            extra={
                "follower_id": follower.id,
                "following_id": following.id,
            },
        )

        return False